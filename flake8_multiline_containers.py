import enum
import textwrap
import token
from tokenize import TokenInfo
from typing import (
    Collection,
    Iterable,
    Iterator,
    List,
    NamedTuple,
    Optional,
    Sequence,
    Tuple,
)

IGNORABLE_TOKEN_TYPES = (token.NL, token.COMMENT, token.ENCODING)
WHITESPACE_TOKEN_TYPES = IGNORABLE_TOKEN_TYPES + (token.INDENT, token.NEWLINE)


class ErrorCode(enum.Enum):
    PL101 = "Multi-line container not broken after opening character"
    PL102 = "Multi-line container not broken before closing character"
    PL110 = "Multi-line container does not close on same column as opening"


Error = Tuple[int, int, str, None]


def _error(line_number: int, column: int, error_code: ErrorCode) -> Error:
    """Format error report such that it's usable by flake8's reporting."""
    return (line_number, column, f'{error_code.name} {error_code.value}', None)


PARENS = {
    '{': '}',
    '(': ')',
    '[': ']',
}


class Range:
    def __init__(
        self,
        start: Tuple[int, TokenInfo],
        end: Tuple[int, TokenInfo],
    ) -> None:
        self.start_idx, self._start = start
        self.end_idx, self._end = end

    def tokens(self, all_tokens: List[TokenInfo]) -> List[TokenInfo]:
        return all_tokens[self.start_idx:self.end_idx + 1]

    @property
    def start_pos(self) -> Tuple[int, int]:
        return self._start.start

    @property
    def end_pos(self) -> Tuple[int, int]:
        return self._end.end

    @property
    def end_start_pos(self) -> Tuple[int, int]:
        return self._end.start

    @property
    def is_single_line(self) -> bool:
        start_line, _ = self.start_pos
        end_line, _ = self.end_pos
        return start_line == end_line

    def is_before(self, other: 'Range') -> bool:
        return self.end_pos < other.start_pos

    def is_after(self, other: 'Range') -> bool:
        return self.start_pos > other.end_pos

    def contains_pos(self, position: Tuple[int, int]) -> bool:
        return self.start_pos <= position <= self.end_pos

    def contains_range(self, other: 'Range') -> bool:
        return (
            self.start_pos <= other.start_pos and
            self.end_pos >= other.end_pos
        )

    def has_overlap(self, other: 'Range') -> bool:
        if self.is_before(other) or self.is_after(other):
            return False

        return True

    def __repr__(self) -> str:
        return '<Range: {!r} - {!r}>'.format(self.start_pos, self.end_pos)


def collect_ranges(tokens: List[TokenInfo]) -> List[Range]:
    ranges = []  # type: List[Range]
    stack = []  # type: List[Tuple[int, TokenInfo]]

    looking_for = None

    for idx, token_info in enumerate(tokens):
        if token_info.string in PARENS.keys():
            stack.append((idx, token_info))
            looking_for = PARENS[token_info.string]
            continue

        if token_info.string == looking_for:
            ranges.append(Range(
                stack.pop(),
                (idx, token_info),
            ))
            looking_for = PARENS[stack[-1][1].string] if stack else None

    if stack:
        raise ValueError("Invalid token stream -- contains mismatched parens")

    return ranges


def filtered_tokens(
    tokens: Iterable[TokenInfo],
    ignore_types: Collection[int] = IGNORABLE_TOKEN_TYPES,
) -> Iterator[TokenInfo]:
    return (x for x in tokens if x.type not in ignore_types)


def get_next_token(
    tokens: Iterable[TokenInfo],
    ignore_types: Collection[int] = IGNORABLE_TOKEN_TYPES,
) -> Optional[TokenInfo]:
    return next(filtered_tokens(tokens), None)


SpanSummary = NamedTuple('SpanSummary', [
    ('start_line_is_broken', bool),
    ('end_line_is_broken', bool),
    ('end_col_matches_start_col', bool),
])


class Span:
    def __init__(self, range_: Range, children: 'List[Span]'):
        self.range = range_
        self.children = children

    @property
    def start_line(self) -> int:
        return self.range.start_pos[0]

    @property
    def end_line(self) -> int:
        return self.range.end_pos[0]

    @property
    def is_single_line(self) -> bool:
        return self.range.is_single_line

    def start_line_is_broken(self, tokens: Sequence[TokenInfo]) -> bool:
        if self.children:
            first_child = self.children[0]
            if first_child.start_line == self.start_line:
                # If the first child starts on the start line, then we defer to
                # whether it has a break or not.
                return not first_child.is_single_line

        # Add 1 so we don't pick up our actual start token
        self_start_idx = self.range.start_idx + 1
        end_idx = self.range.end_idx

        start_tokens = tokens[self_start_idx:end_idx]
        next_token = get_next_token(start_tokens)

        if not next_token:
            # If there isn't a next token then we treat this like a suitable
            # line break being present.
            return True

        return next_token.start[0] != self.start_line

    def get_end_tokens(self, tokens: Sequence[TokenInfo]) -> Sequence[TokenInfo]:
        self_end_idx = self.range.end_idx

        # Add 1 so we don't pick up the actual start token
        start_idx = (
            self.children[-1].range.end_idx
            if self.children and not self.children[-1].is_single_line
            else self.range.start_idx
        ) + 1

        return tokens[start_idx:self_end_idx]

    def end_line_is_broken(self, tokens: Sequence[TokenInfo]) -> bool:
        if self.children:
            last_child = self.children[-1]
            if last_child.end_line == self.end_line:
                # If the last child ends on the last line, then we defer to
                # whether it has a break or not.
                return not last_child.is_single_line

        end_tokens = self.get_end_tokens(tokens)
        prev_token = get_next_token(reversed(end_tokens))

        if not prev_token:
            # If there isn't a previous token then we treat this like a suitable
            # line break being present.
            return True

        return prev_token.start[0] != self.end_line

    def end_col_matches_start_col(self, tokens: Sequence[TokenInfo]) -> bool:
        start_line, start_col = self.range.start_pos
        _, end_col = self.range.end_start_pos

        preceding_tokens = tokens[:self.range.start_idx]

        if preceding_tokens:
            for tok in filtered_tokens(
                reversed(preceding_tokens),
                ignore_types=WHITESPACE_TOKEN_TYPES,
            ):
                line, col = tok.start
                if line == start_line:
                    start_col = col
                else:
                    break

        end_tokens = self.get_end_tokens(tokens)
        if not end_tokens:
            # If there are no preceding tokens on our end line then that
            # indicates we're hugging another span, which is fine.
            return True

        return start_col == end_col

    def analyse_tokens(self, tokens: List[TokenInfo]) -> SpanSummary:
        return SpanSummary(
            self.start_line_is_broken(tokens),
            self.end_line_is_broken(tokens),
            self.end_col_matches_start_col(tokens),
        )

    def __repr__(self) -> str:
        return '<Span: {!r} - {!r} | {} children>'.format(
            self.range.start_pos,
            self.range.end_pos,
            len(self.children),
        )


def pretty_spans(spans: Iterable[Span], *, prefix: str = '    ') -> str:
    return textwrap.indent('\n'.join(pretty_span(x) for x in spans), prefix)


def pretty_span(span: Span) -> str:
    return 'Span: {!r} - {!r}{}'.format(
        span.range.start_pos,
        span.range.end_pos,
        ':\n' + pretty_spans(span.children) if span.children else '',
    )


def collect_spans(ranges: List[Range]) -> List[Span]:
    root_spans = []  # type: List[Span]

    stack = []  # type: List[Span]

    for range_ in sorted(ranges, key=lambda x: x.start_pos):
        span = Span(range_, [])

        while stack:
            if stack[-1].range.contains_range(range_):
                stack[-1].children.append(span)
                stack.append(span)
                break

            else:
                stack.pop()

        if not stack:
            root_spans.append(span)
            stack.append(span)
            continue

    return root_spans


class MultilineContainers:
    """Ensure the consistency of multiline dict and list style."""

    name = 'flake8_multiline_containers'
    version = '0.0.15'

    def __init__(
        self,
        # We don't actually want the AST, however this is needed to indicate to
        # flake8 that we're a whole-file plugin and to register us properly.
        tree: object,
        file_tokens: List[TokenInfo],
        debug: bool = False,
    ) -> None:
        self.tokens = file_tokens

        self.debug = debug

    def analyse_span(self, span: Span) -> Iterator[Error]:
        if span.is_single_line:
            return

        (start_line, start_col) = span.range.start_pos
        (end_line, end_col) = span.range.end_pos

        span_summary = span.analyse_tokens(self.tokens)

        if not span_summary.start_line_is_broken:
            yield _error(start_line, start_col, ErrorCode.PL101)

        for child in span.children:
            yield from self.analyse_span(child)

        if not span_summary.end_line_is_broken:
            yield _error(end_line, end_col, ErrorCode.PL102)

        elif not span_summary.end_col_matches_start_col:
            yield _error(end_line, end_col, ErrorCode.PL110)

    def __iter__(self) -> Iterator[Error]:
        """Entry point for the plugin."""

        spans = collect_spans(collect_ranges(self.tokens))

        if self.debug:
            print(pretty_spans(spans, prefix=''))

        for span in spans:
            yield from self.analyse_span(span)

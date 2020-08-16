import enum
from tokenize import TokenInfo
from typing import Iterable, List, NamedTuple, Optional, Sequence, Tuple

import attr


class ErrorCode(enum.Enum):
    JS101 = "Multi-line container not broken after opening character"
    JS102 = "Multi-line container does not close on same column as opening"


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


ChildTokenSummary = NamedTuple('ChildTokenSummary', [
    ('on_start_line', Optional[List[TokenInfo]]),
    ('on_end_line', Optional[List[TokenInfo]]),
])


class Span:
    def __init__(self, range_: Range, children: 'List[Span]'):
        self.range = range_
        self.children = children

    def analyse_start(self, tokens: Sequence[TokenInfo]) -> bool:
        self_start_line, _ = self.range.start_pos
        self_start_idx = self.range.start_idx

        first_child_start_idx = (
            self.children[0].range.start_idx
            if self.children
            else None
        )

        start_tokens = tokens[self_start_idx:first_child_start_idx]

        return bool(
            start_tokens and
            start_tokens[0].start[0] == self_start_line
        )

    def analyse_end(self, tokens: Sequence[TokenInfo]) -> bool:
        self_end_line, _ = self.range.end_pos
        self_end_idx = self.range.end_idx

        first_child_end_idx = (
            self.children[0].range.end_idx
            if self.children
            else None
        )

        end_tokens = tokens[first_child_end_idx:self_end_idx]

        return bool(
            end_tokens and
            end_tokens[-1].end[0] == self_end_line
        )

    def analyse_tokens(self, tokens: List[TokenInfo]) -> ChildTokenSummary:
        return ChildTokenSummary(
            self.analyse_start(tokens),
            self.analyse_end(tokens),
        )

    def __repr__(self) -> str:
        return '<Span: {!r} - {!r} | {} children>'.format(
            self.range.start_pos,
            self.range.end_pos,
            len(self.children),
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


@attr.s(hash=False)
class MultilineContainers:
    """Ensure the consistency of multiline dict and list style."""

    name = 'flake8_multiline_containers'
    version = '0.0.15'

    logical_line = attr.ib(default=None)
    tokens = attr.ib(default=None)  # type: Iterable[TokenInfo]

    errors = attr.ib(factory=list)

    def analyse_span(self, span: Span) -> List[Error]:
        (start_line, start_col) = span.range.start_pos
        (end_line, end_col) = span.range.end_pos

        if start_line == end_line:
            return []

        child_token_summary = span.analyse_tokens(self.tokens)

        errors = []
        if child_token_summary.on_start_line:
            errors.append(_error(start_line, start_col, ErrorCode.JS101))

        if child_token_summary.on_end_line:
            errors.append(_error(end_line, end_col, ErrorCode.JS101))

        return errors

    def __iter__(self):
        """Entry point for the plugin."""

        spans = collect_spans(collect_ranges(self.tokens))
        print(spans)

        return iter(self.errors)

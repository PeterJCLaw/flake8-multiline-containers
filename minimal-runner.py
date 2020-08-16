#!/usr/bin/env python

import argparse
import io
import pathlib
import pprint
import time
import tokenize

from flake8_multiline_containers import MultilineContainers


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='+', type=pathlib.Path)
    return parser.parse_args()


def main(args: argparse.Namespace) -> None:
    start = time.time()

    for path in args.files:
        tokens = tokenize.tokenize(io.BytesIO(path.read_bytes()).readline)
        checker = MultilineContainers(tokens=tokens, logical_line=None)
        pprint.pprint(list(checker))

    print(time.time() - start)


if __name__ == '__main__':
    main(parse_args())

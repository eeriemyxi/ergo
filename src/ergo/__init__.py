import argparse
import logging
import typing

from ergo import lexer, util

log = logging.getLogger(__name__)


def process_file(file: typing.TextIO) -> None:
    text = util.CustomStringIO(file.read())
    ast = lexer.tokenize(text)
    util._pprint(ast)


def main() -> None:
    logging.basicConfig(level="DEBUG")

    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=argparse.FileType("r"))
    args = parser.parse_args()

    if args.file:
        process_file(args.file)


if __name__ == "__init__":
    main()

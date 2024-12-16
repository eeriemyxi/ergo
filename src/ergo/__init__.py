import argparse
import logging
import typing

from ergo import lexer, parser, util

log = logging.getLogger(__name__)


def process_file(file: typing.TextIO) -> None:
    text = util.CustomStringIO(file.read())
    tokens = lexer.make_tokens(text)
    ast = parser.make_ast(tokens)
    util._pprint(ast)


def repl():
    while True:
        try:
            text = util.CustomStringIO(input(">>> "))
        except EOFError:
            print()
            exit()
        except KeyboardInterrupt:
            print()
            continue
        tokens = lexer.make_tokens(text)
        ast = parser.make_ast(tokens)
        util._pprint(ast)


def main() -> None:
    logging.basicConfig(level="DEBUG")

    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=argparse.FileType("r"), nargs="?")
    args = parser.parse_args()

    if args.file:
        process_file(args.file)
    else:
        repl()


if __name__ == "__init__":
    main()

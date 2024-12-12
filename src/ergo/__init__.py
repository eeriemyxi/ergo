import argparse
import io
import logging
import typing
from dataclasses import dataclass
from enum import Enum, auto


class TokenType(Enum):
    IDENT = auto()
    STRING = auto()
    KEY_PREFIX = auto()
    KEY = auto()


@dataclass
class Token:
    type: TokenType
    literal: str


log = logging.getLogger(__name__)


class CustomTextIO(io.StringIO):
    def peek(self, n: int = 1) -> str:
        opos = self.tell()
        char = self.read(n)
        self.seek(opos)
        return char


def _pprint(*args, **kwargs):
    import pprint

    pprint.pprint(*args, **kwargs)


def make_ast(tokens: list[Token]) -> list[Token]:
    i = 0
    tree = []
    while i < len(tokens):
        token = tokens[i]
        if token.type == TokenType.KEY_PREFIX:
            if i + 1 >= len(tokens):
                log.error("Reached EOF before parsing key.")
                break
            if tokens[i + 1].type != TokenType.IDENT:
                log.error(
                    "Key must be a valid identifier, not '%s'", tokens[i + 1].literal
                )
                break
            tree.append(Token(TokenType.KEY, tokens[i + 1].literal))
            i += 1
        else:
            tree.append(token)
        i += 1
    return tree


def isident(c: str) -> bool:
    return c.isalpha() or c == "-"


def process_text(text: CustomTextIO) -> None:
    tokens = []

    while True:
        c = text.read(1)

        if c.isalpha():
            ident = c
            while text.peek() != " ":
                c = text.read(1)
                if not c.isalnum() and c != "-":
                    log.error("Invalid identifier %s", repr(ident + c))
                    exit(1)
                ident += c
            tokens.append(Token(TokenType.IDENT, ident))

        if c == "." and text.peek() == ".":
            text.read(1)
            string = ""
            while True:
                c = text.read(1)
                if c == "":
                    log.error("Unterminated string '%s'", repr(string + c))
                    exit(1)
                if c == "." and text.peek() == ".":
                    text.read(1)
                    if text.peek() == ".":
                        string += text.read(1)
                    tokens.append(Token(TokenType.STRING, string))
                    break
                string += c

        if c == "." and text.peek().isalnum():
            tokens.append(Token(TokenType.KEY_PREFIX, c))

        if c == "":
            log.debug("Reached end of file.")
            break

    return make_ast(tokens)


def process_file(file: typing.TextIO) -> None:
    text = CustomTextIO(file.read())
    ast = process_text(text)
    _pprint(ast)


def main() -> None:
    logging.basicConfig(level="DEBUG")

    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=argparse.FileType("r"))
    args = parser.parse_args()

    if args.file:
        process_file(args.file)


if __name__ == "__init__":
    main()

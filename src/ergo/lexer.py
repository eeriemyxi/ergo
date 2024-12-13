import logging

from ergo import parser, tokens, util

log = logging.getLogger(__name__)


def tokenize(text: util.CustomStringIO) -> None:
    tokens_list = []

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
            tokens_list.append(tokens.Token(tokens.TokenType.IDENT, ident))

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
                    tokens_list.append(tokens.Token(tokens.TokenType.STRING, string))
                    break
                string += c

        if c == "." and text.peek().isalnum():
            tokens_list.append(tokens.Token(tokens.TokenType.KEY_PREFIX, c))

        if c == "":
            log.debug("Reached end of file.")
            break

    return parser.make_ast(tokens_list)

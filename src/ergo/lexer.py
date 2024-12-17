import logging

from ergo import tokens, util

log = logging.getLogger(__name__)


def lex_identifier(text):
    log.debug("Parsing an identifier")
    ident = ""

    while not text.peek().isspace():
        c = text.read(1)
        if c == "":
            break
        if not c.isalnum() and c != "-":
            log.error("Invalid identifier: %s", repr(ident + c))
            exit(1)
        ident += c

    text.read(1)  # the space

    return ident


def lex_number(text):
    log.debug("Parsing a number")
    number = ""
    while not text.peek().isspace():
        c = text.read(1)
        if c == "":
            break
        if not c.isdigit() and c != ".":
            log.error("Invalid number: %s", number + c)
            exit(1)
        number += c
    try:
        convnum = float(number)
    except ValueError:
        log.error("Invalid number: %s", number + c)
        exit(1)

    text.read(1)  # the space

    return convnum


def lex_string(text):
    log.debug("Parsing a string")
    string = ""
    while True:
        c = text.read(1)
        if c == "":
            log.error("Unterminated string '%s'", repr(string + c))
            exit(1)
        if c == "\\":
            if text.peek() == ".":
                string += ".."
            elif text.peek() == "\\":
                string += "\\"
            text.read(1)
            continue
        if c == "." and text.peek() == ".":
            text.read(1)
            if text.peek() == ".":
                string += text.read(1)
            text.read(1)  # the last dot
            break
        string += c

    return string


def make_tokens(text: util.CustomStringIO) -> None:
    tokens_list = []

    while True:
        if text.peek().isalnum():
            ident = lex_identifier(text)
            tokens_list.append(tokens.Token(tokens.TokenType.IDENT, ident))

        elif text.peek().isdigit():
            number = lex_number(text)
            tokens_list.append(tokens.Token(tokens.TokenType.NUMBER, number))

        elif text.peek() == ".":
            text.read(1)
            if text.peek() == ".":
                text.read(1)
                string = lex_string(text)
                tokens_list.append(tokens.Token(tokens.TokenType.STRING, string))
            elif text.peek().isalnum():
                tokens_list.append(tokens.Token(tokens.TokenType.KEY_PREFIX, "."))

        elif text.peek() == "":
            log.debug("Reached end of file.")
            break

    return tokens_list

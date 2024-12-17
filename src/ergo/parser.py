import logging

from ergo import tokens

log = logging.getLogger(__name__)


def make_ast(tokens_list: list[tokens.Token]) -> list[tokens.Token]:
    i = 0
    tree = []
    while i < len(tokens_list):
        token = tokens_list[i]
        if token.type == tokens.TokenType.KEY_PREFIX:
            if i + 1 >= len(tokens_list):
                log.error("Reached EOF before parsing key.")
                break
            if tokens_list[i + 1].type != tokens.TokenType.IDENT:
                log.error(
                    "Key must be a valid identifier, not '%s'",
                    tokens_list[i + 1].literal,
                )
                break
            token = tokens.Token(tokens.TokenType.KEY, tokens_list[i + 1].literal)
            tree.append(token)
            i += 1
        elif token.type in (tokens.TokenType.STRING, tokens.TokenType.NUMBER):
            if len(tokens_list) == 1:
                tree.append(tokens.Token(tokens.TokenType.STRING, token.literal))
            elif tree[-1].type == tokens.TokenType.KEY:
                key = tree[-1]
                key.children.append(token)
            else:
                tree.append(tokens.Token(tokens.TokenType.ARG, token.literal))
        else:
            tree.append(token)
        i += 1
    return tree

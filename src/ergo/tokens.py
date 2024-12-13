from dataclasses import dataclass, field
from enum import Enum, auto


class TokenType(Enum):
    IDENT = auto()
    STRING = auto()
    NUMBER = auto()
    KEY_PREFIX = auto()
    KEY = auto()
    ARG = auto()


@dataclass
class Token:
    type: TokenType
    literal: str
    children: list[str] = field(default_factory=list)

from enum import Enum

RESERVED_WORDS = ['int', 'char', 'if', 'else', 'for', 'while', 'return']

BIN_OPS = ['+', '-', '*', '/']

# TODO: Igualdade é relacional?
REL_OP = ['<', '>', '==', '!=', '<=', '>=', '=']

LOGIC_OP = ['&&', '||']

SEPARATORS = ['(', ')', '{', '}', '[', ']', ';', ',']

ALL_ELEMENTS = BIN_OPS + REL_OP + LOGIC_OP + SEPARATORS


class STATES(Enum):
    INITIAL = 0
    COMMENT = 1
    IDENTIFIER = 2
    LITERAL = 3
    NUMERIC = 4

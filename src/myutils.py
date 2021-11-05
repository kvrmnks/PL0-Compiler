from enum import Enum, auto, unique

MAGIC = 16


@unique
class TokenType(Enum):
    ASSIGN = 0  # :=
    PLUS = 1  # +
    MINUS = 2  # -
    TIMES = 3  # *
    DIVIDE = 4  # /
    EQUAL = 5  # =
    NEQUAL = 6  # #
    LESS = 7  # <
    LESS_OR_EQUAL = 8  # <=
    GREATER = 9  # >
    GREATER_OR_EQUAL = 10  # >=
    # OPERATOR = auto()  # := + - * / = # < <= > >=
    # SYMBLE = auto()  # ; , .
    SEMICOLON = 11  # ;
    COMMA = 12  # ,
    DOT = 13  # .
    LEFT_PARENTHESES = 14  # (
    RIGHT_PARENTHESES = 15  # )
    CONST = MAGIC + 0
    VAR = MAGIC + 1
    PROCEDURE = MAGIC + 2
    BEGIN = MAGIC + 3
    END = MAGIC + 4
    ODD = MAGIC + 5
    IF = MAGIC + 6
    THEN = MAGIC + 7
    CALL = MAGIC + 8
    WHILE = MAGIC + 9
    DO = MAGIC + 10
    READ = MAGIC + 11
    WRITE = MAGIC + 12
    # CONST VAR procedure begin end odd if then call while do read write
    IDENTIFIER = MAGIC + 13  # user defined
    NUMBER = MAGIC + 14  # just integer number...


class Token:
    def __init__(self, t: TokenType, identifier: str, number: int):
        self.token_type = t
        self.identifier = identifier
        self.number = number


CHARACTER_LIST = [
    ":=", "+", "-", "*", "/", "=", "#", "<", "<=", ">", ">=",
    ";", ",", ".", "(", ")"
]

KEYWORD_LIST = [
    "const", "var", "procedure", "begin", "end", "odd", "if", "then", "call", "while",
    "do", "read", "write"
]


def str_is_space(s: str) -> bool:
    return ord(s[0]) <= 32


def str_is_alphabet(s: str) -> bool:
    if ord('a') <= ord(s[0]) <= ord('z') or ord('A') <= ord(s[0]) <= ord('Z'):
        return True
    return False


def str_is_number(s: str) -> bool:
    return ord('0') <= ord(s[0]) <= ord('9')


def str_is_bi_char(s: str) -> bool:
    return s == "<" or s == ">" or s == ":"


def str_is_character(s: str) -> bool:
    for x in CHARACTER_LIST:
        if s == x[0]:
            return True
    return False


def str_is_legal(s: str) -> bool:
    return len(s) == 1 and (str_is_space(s) \
                            or str_is_alphabet(s) \
                            or str_is_number(s) \
                            or str_is_character(s) \
                            or str_is_bi_char(s))

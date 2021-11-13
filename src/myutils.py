from enum import Enum, auto, unique

MAGIC = 16


@unique
class TokenType(Enum):
    ASSIGN = ':='  # :=
    PLUS = '+'  # +
    MINUS = '-'  # -
    TIMES = '*'  # *
    DIVIDE = '/'  # /
    EQUAL = '='  # =
    NEQUAL = '#'  # #
    LESS = '<'  # <
    LESS_OR_EQUAL = '<='  # <=
    GREATER = '>'  # >
    GREATER_OR_EQUAL = '>='  # >=
    DOLLER = '$'
    # OPERATOR = auto()  # := + - * / = # < <= > >=
    # SYMBLE = auto()  # ; , .
    SEMICOLON = ';'  # ;
    COMMA = ','  # ,
    DOT = '.'  # .
    LEFT_PARENTHESES = '('  # (
    RIGHT_PARENTHESES = ')'  # )
    CONST = 'const'
    VAR = 'var'
    PROCEDURE = 'procedure'
    BEGIN = 'begin'
    END = 'end'
    ODD = 'odd'
    IF = 'if'
    THEN = 'then'
    CALL = 'call'
    WHILE = 'while'
    DO = 'do'
    READ = 'read'
    WRITE = 'write'
    # CONST VAR procedure begin end odd if then call while do read write
    IDENTIFIER = 'id'  # MAGIC + 13  # user defined
    NUMBER = 'num'  # MAGIC + 14  # just integer number...


class Token:
    def __init__(self, t: TokenType, identifier: str, number: int):
        self.token_type = t
        self.identifier = identifier
        self.number = number

    def __str__(self):
        return "{type: %s id: %s num: %s}" % (self.token_type, self.identifier, self.number)

    def __repr__(self):
        return self.__str__()


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

from enum import Enum, auto, unique

@unique
class TokenType(Enum):
    KEYWORD = auto() # CONST VAR procedure begin end odd if then call while read write
    IDENTIFIER = auto() # user defined
    NUMBER = auto() # just integer number...
    OPERATOR = auto() # := + - * / = # < <= > >=
    SYMBLE = auto() # { } ; , .

class Token:
    def __init__(self, t: TokenType, identifier: str, number: int):
        self.token_type = t
        self.identifier = identifier
        self.number = number
from myutils import *


class InputStream:
    def __init__(self, path: str):
        self.file = open(path, 'r')
        self.stack = []

    def eof(self) -> bool:
        if len(self.stack) > 0:
            return False
        else:
            return not self.file.readable()

    def push_back(self, s: str):
        self.stack.append(s)

    def pop(self):
        if len(self.stack) > 0:
            self.stack = self.stack[:-1]
        else:
            self.file.read(1)

    def peak(self) -> str:
        if len(self.stack) > 0:
            return self.stack[len(self.stack) - 1]
        else:
            self.stack.append(self.file.read(1))
            return self.stack[len(self.stack) - 1]


class Lexer:
    def __init__(self, from_path, to_path):
        self.from_path = from_path
        self.to_path = to_path
        self.stream = InputStream(from_path)
        self.state = 0
        self.end = False

    def has_next(self) -> bool:
        return not self.stream.eof()

    def deal_with_bi_char(self, partial_token: Token):
        s = self.stream.peak()
        self.stream.pop()
        if self.stream.eof():
            print('error in bilateral char')
            exit(-1)
        next_s = self.stream.peak()
        if s == ":":
            if next_s == "=":
                partial_token.token_type = TokenType.ASSIGN
            else:
                print('error behind :')
                exit(-1)
        elif s == '>':
            if next_s == '=':
                partial_token.token_type = TokenType.GREATER_OR_EQUAL
            else:
                partial_token.token_type = TokenType.GREATER
                self.stream.push_back(s)
        elif s == '<':
            if next_s == '=':
                partial_token.token_type = TokenType.LESS_OR_EQUAL
            else:
                partial_token.token_type = TokenType.LESS
                self.stream.push_back(s)

    def deal_with_one_side_char(self, partial_token: Token):
        loc = -1
        s = self.stream.peak()
        for i in range(len(CHARACTER_LIST)):
            if s == CHARACTER_LIST[i]:
                loc = i
                break
        if loc == -1:
            print('error at one side')
            exit(-1)
        if s == '.':
            partial_token.token_type = TokenType('$')
        else:
            partial_token.token_type = TokenType(CHARACTER_LIST[loc])

    def deal_with_state0(self, partial_token: Token):
        s = self.stream.peak()
        # print(s)
        if str_is_space(s):
            self.state = 0
        elif str_is_number(s):
            partial_token.number = partial_token.number * 10 + (ord(s[0]) - ord('0'))
            self.state = 1
        elif str_is_alphabet(s):
            self.state = 2
            partial_token.identifier += s
        elif str_is_character(s):
            self.state = 0
            # print(s, str_is_bi_char(s))
            if str_is_bi_char(s):
                self.deal_with_bi_char(partial_token)
            else:
                self.deal_with_one_side_char(partial_token)

    def deal_with_state1(self, partial_token: Token):
        s = self.stream.peak()
        if str_is_number(s):
            self.state = 1
            partial_token.number = partial_token.number * 10 + (ord(s[0]) - ord('0'))
        else:
            self.state = 0
            partial_token.token_type = TokenType.NUMBER
            self.stream.push_back(s)

    def deal_with_state2(self, partial_token: Token):
        s = self.stream.peak()
        if str_is_number(s) or str_is_alphabet(s):
            partial_token.identifier += s
            self.state = 2
        else:
            self.state = 0
            loc = -1
            for i in range(len(KEYWORD_LIST)):
                if KEYWORD_LIST[i] == partial_token.identifier:
                    loc = i
                    break
            if loc == -1:
                partial_token.token_type = TokenType.IDENTIFIER
                self.stream.push_back(s)
            else:
                partial_token.token_type = TokenType(KEYWORD_LIST[loc])  # 14 is magic number !
                self.stream.push_back(s)

    def get_next(self) -> Token:

        ret = Token(None, "", 0)

        while True:

            if self.stream.eof():
                break

            s = self.stream.peak()

            if s == "":
                if not self.end:
                    self.end = True
                    self.stream.push_back(" ")
                    s = " "
                else:
                    break
                # break

            if not str_is_legal(s):
                print(len(s), ord(s[0]), s)
                print("非法字符")
                exit(-1)

            if self.state == 0:
                self.deal_with_state0(ret)
            elif self.state == 1:
                self.deal_with_state1(ret)
            elif self.state == 2:
                self.deal_with_state2(ret)

            self.stream.pop()
            # print(self.stream.stack)
            if self.state == 0 and (ret.token_type is not None):
                break

        return ret


if __name__ == "__main__":
    # a = Lexer("../PL0_code/PL0_code3.in", "")
    a = Lexer("../PL0_code/PL0_code.in", "")
    while a.has_next():
        t = a.get_next()
        print(t.token_type,"\t", t.number,"\t", t.identifier)
        if t.token_type is None:
            break

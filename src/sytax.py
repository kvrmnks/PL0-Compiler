from LR_table import SLRParser
from LR1_table import LR1Parser
from lexer import Lexer
from Grammar import Grammar
from myutils import Token


class Syntax:
    def __init__(self, code_path: str, grammar: str):
        self.lexer = Lexer(code_path, "")
        self.grammar = Grammar(grammar)
        self.parser = LR1Parser(self.grammar)
        # self.parser = SLRParser(grammar)
        print(self.parser.G_indexed)
        self.parsing_table = self.parser.parse_table
        self.state_stack = [0]

    def process_one_hop(self, param: str):
        # print(self.parsing_table[self.state_stack[-1]])
        cmd = str(self.parsing_table[self.state_stack[-1]][param])
        print(self.state_stack, cmd, param)
        if cmd == '':
            print("No such action!")
            exit(-1)
        elif cmd[0] == 'a':
            print('Finish!')
        elif cmd[0] == 's':
            self.state_stack.append(int(cmd[1:]))
        elif cmd[0] == 'r':
            print(self.parser.G_indexed[int(cmd[1:])])
            tp = self.parser.G_indexed[int(cmd[1:])][1]  # A -> B, tp = B
            lp = self.parser.G_indexed[int(cmd[1:])][0]
            if tp[0] != '^':
                self.state_stack = self.state_stack[0:len(self.state_stack) - len(tp)]
            self.process_one_hop(lp)
            self.process_one_hop(param)
        else:
            self.state_stack.append(int(cmd))

    def process(self):
        while self.lexer.has_next():
            t = self.lexer.get_next()
            if t.token_type is None:
                break
            self.process_one_hop(t.token_type.value)

            # cmd = parsing_table[state_stack[-1]][t.token_type.value]


if __name__ == '__main__':
    s = Syntax("../PL0_code/PL0_code.in", open("./grammar.g").read())
    s.process()

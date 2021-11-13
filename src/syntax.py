from LR_table import SLRParser
from LR1_table import LR1Parser
from lexer import Lexer
from Grammar import Grammar
from myutils import Token
from InterRep import InterRep


class Syntax:
    def __init__(self, code_path: str, grammar: str):
        self.inter_rep = InterRep()
        self.lexer = Lexer(code_path, "")
        self.grammar = Grammar(grammar)
        # self.parser = LR1Parser(self.grammar)
        self.parser = SLRParser(self.grammar)
        # print(self.parser.G_indexed)
        self.parsing_table = self.parser.parse_table
        self.state_stack = [0]
        self.readable_stack = []
        self.props_stack = []  # 存放各种属性
        # print(self.parser.parse_table)
        # for x in self.parser.parse_table.keys():
        #     print(x, self.parser.parse_table[x])

    # def subprocess_add_procedure

    def process_inter_rep(self, cmd: str, tk: Token):
        if cmd == 'IDid':
            pass
            # print(self.props_stack[-1].identifier)
            # ID -> id

        if cmd == "PROC_HEADprocedureID;":
            # PROC_HEAD -> procedure ID ;
            print("PROC_HEAD -> procedure ID")
            for x in self.props_stack:
                print(x.token_type)
            # print(self.props_stack.token_type)
        elif cmd == 'IDid':
            print('parse id', tk)

    def process_one_hop(self, param: str, tk: Token):
        # print(self.parsing_table[self.state_stack[-1]])
        cmd = str(self.parsing_table[self.state_stack[-1]][param])
        # print(self.readable_stack, cmd, param)
        if cmd == '':
            print("No such action!")
            exit(-1)
        elif cmd[0] == 'a':
            print('Finish!')
        elif cmd[0] == 's':
            self.state_stack.append(int(cmd[1:]))
            self.readable_stack.append(param)
            # self.props_stack.append(tk)

        elif cmd[0] == 'r':
            # print(self.parser.G_indexed[int(cmd[1:])])
            tp = self.parser.G_indexed[int(cmd[1:])][1]  # A -> B, tp = B
            lp = self.parser.G_indexed[int(cmd[1:])][0]
            # print(lp, " ".join(tp))
            self.process_inter_rep(lp + "".join(tp), tk)

            if tp[0] != '^':
                self.state_stack = self.state_stack[0:len(self.state_stack) - len(tp)]
                self.readable_stack = self.readable_stack[0: len(self.readable_stack) - len(tp)]
                # self.props_stack = self.props_stack[0: len(self.props_stack) - len(tp)]

            self.process_one_hop(lp, tk)
            self.process_one_hop(param, tk)
        else:
            self.state_stack.append(int(cmd))
            self.readable_stack.append(param)
            # self.props_stack.append(tk)

    def process(self):
        while self.lexer.has_next():
            t = self.lexer.get_next()
            if t.token_type is None:
                break
            # print('lexer', t.token_type, t.number, t.identifier)
            self.process_one_hop(t.token_type.value, t)

            # cmd = parsing_table[state_stack[-1]][t.token_type.value]

    def iprocess(self):
        while True:
            t = input()
            self.process_one_hop(t, None)


if __name__ == '__main__':
    s = Syntax("../PL0_code/PL0_code.in", open("./grammar.g").read())
    s.process()

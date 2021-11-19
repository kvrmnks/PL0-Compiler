from LR_table import SLRParser
from LR1_table import LR1Parser
from lexer import Lexer
from Grammar import Grammar
from myutils import Token, TokenType
from InterRep import InterRep
from LogWriter import LogWriter


class Syntax:
    def __init__(self, code_path: str, grammar: str):

        self.inter_rep = InterRep()  # 用于生成中间代码
        self.inter_rep.add_procedure("_global", 0)
        self.logWriter = LogWriter('abab.txt')
        self.lexer = Lexer(code_path, "")
        self.grammar = Grammar(grammar)
        self.parser = LR1Parser(self.grammar)
        self.global_address_counter = 0  # 记录生成的地址
        # self.parser = SLRParser(self.grammar)
        # print(self.parser.G_indexed)
        self.parsing_table = self.parser.parse_table
        self.state_stack = [0]
        self.readable_stack = []
        self.props_stack = []  # 存放各种属性
        # self.inter_rep
        # print(self.parser.parse_table)
        # for x in self.parser.parse_table.keys():
        #     print(x, self.parser.parse_table[x])

    # def subprocess_add_procedure
    def check_props_stack(self, token_types: list) -> bool:
        if len(self.props_stack) < len(token_types):
            print('panic in check props_stack')
            exit(-1)
        for (i, x) in enumerate(token_types):
            if self.props_stack[-(len(token_types) - i)].token_type != x:
                print('panic in check props_stack')
                exit(-1)
        return False

    def process_inter_rep(self, cmd: str):
        print(cmd, self.props_stack)
        # print(cmd)
        if cmd == "PROC_HEAD -> procedure ID ;":
            print("PROC_HEAD -> procedure ID ;")
            self.check_props_stack([TokenType.PROCEDURE, TokenType.IDENTIFIER, TokenType.SEMICOLON])
            self.inter_rep.add_procedure(self.props_stack[-2].identifier, self.inter_rep.current_procedure.level + 1)
            self.props_stack = self.props_stack[: -3]

        elif cmd == 'CONST_DEF -> ID = UINT':
            print('CONST_DEF -> ID = UINT')
            self.check_props_stack([TokenType.IDENTIFIER, TokenType.EQUAL, TokenType.NUMBER])
            # print(self.props_stack)
            self.inter_rep.add_const(self.props_stack[-3].identifier, self.props_stack[-1].number)
            self.props_stack = self.props_stack[: -3]

        elif cmd == 'VARIABLE_ -> var ID':
            print('VARIABLE_ -> var ID')
            self.check_props_stack([TokenType.VAR, TokenType.IDENTIFIER])
            self.inter_rep.add_var(self.props_stack[-1].identifier)
            self.props_stack = self.props_stack[: -2]
            # print(self.props_stack)

        elif cmd == 'VARIABLE_ -> VARIABLE_ , ID':
            print('VARIABLE_ -> VARIABLE_ , ID')
            self.check_props_stack([TokenType.COMMA, TokenType.IDENTIFIER])
            self.inter_rep.add_var(self.props_stack[-1].identifier)
            self.props_stack = self.props_stack[: -2]
            # print(self.props_stack)

        elif cmd == 'FACTOR -> ID':
            print('FACTOR -> ID')
            self.check_props_stack([TokenType.IDENTIFIER])
            ret = self.inter_rep.find_by_name(self.props_stack[-1].identifier)
            if ret is None:
                print('panic in factor -> id')
                exit(-1)
            # print(ret)
            if ret[2] == 0:
                # 常量
                self.logWriter.write('LIT', 0, ret[1])
            else:
                # 变量
                if ret[0] > 1:
                    print('乱花渐欲迷人眼，浅草才能没马蹄')
                    exit(-1)
                self.logWriter.write("LOD", ret[0], ret[1][1])
            # self.props_stack[-1] = Token(TokenType.NUMBER, "", ret[0])
            # print(self.props_stack)
        elif cmd == 'FACTOR -> UINT':
            print('FACTOR -> UINT')
            self.check_props_stack([TokenType.NUMBER])
            self.logWriter.write('LIT', 0, self.props_stack[-1].number)

        elif cmd == 'FACTOR -> ( EXPR )':
            print('FACTOR -> ( EXPR )')
            self.check_props_stack([TokenType.LEFT_PARENTHESES, TokenType.IDENTIFIER, TokenType.RIGHT_PARENTHESES])
            tmp = self.props_stack[-2]
            self.props_stack = self.props_stack[:-3]
            self.props_stack.append(tmp)
            # print(self.props_stack)
        elif cmd == 'SUBPROG -> CONST VARIABLE PROCEDURE M_STATEMENT STATEMENT':
            print('SUBPROG -> CONST VARIABLE PROCEDURE M_STATEMENT STATEMENT')
            if self.inter_rep.current_procedure.father != "":
                self.inter_rep.current_procedure = self.inter_rep.procedure_dict[
                    self.inter_rep.current_procedure.father]
            # print(self.props_stack)
        elif cmd == 'M_STATEMENT -> ^':
            print('M_STATEMENT -> ^')
            volumn = 3 + len(self.inter_rep.current_procedure.var_dict)
            self.inter_rep.current_procedure.address = self.logWriter.total_line
            self.logWriter.write('int', '0', volumn)

        elif cmd == 'EXPR -> EXPR PLUS_MINUS ITEM':
            print('EXPR -> EXPR PLUS_MINUS ITEM')
            # print(s)
            print(self.props_stack)
            if self.props_stack[-2].token_type == TokenType.MINUS:
                self.logWriter.write('OPR', 0, 3)
            else:
                self.logWriter.write('OPR', 0, 2)
            self.props_stack = self.props_stack[:-2]
            # print('int', '0', volumn)
        elif cmd == 'EXPR -> PLUS_MINUS ITEM':
            print('EXPR -> PLUS_MINUS ITEM')
            print(self.props_stack[-2])
            if self.props_stack[-2].token_type == TokenType.MINUS:
                self.logWriter.write('OPR', 0, 1)
            self.props_stack = self.props_stack[:-1]
        # elif cmd == 'ITEM -> ITEM MUL_DIV FACTOR'
        elif cmd == 'CALL -> call ID':
            print('CALL -> call ID')
            # self.props_stack[-1].identifier
            tmp_p = self.inter_rep.current_procedure
            while True:
                # 得到 tmp_p 的 儿子们
                ps = [self.inter_rep.procedure_dict[x] for x in self.inter_rep.procedure_dict.keys() if self.inter_rep.procedure_dict[x].father == tmp_p.name]
                nps = [x for x in ps if x.name == self.props_stack[-1].identifier]
                if len(nps) == 0:
                    if tmp_p.father == "":
                        print('调用了不存在的procedure')
                        exit(-1)
                    tmp_p = self.inter_rep.procedure_dict[tmp_p.father]
                else:
                    nps = nps[0]
                    self.logWriter.write('call', self.inter_rep.current_procedure.level + 1 - nps.level, nps.address)
                    break
        elif cmd == 'ASSIGN -> ID := EXPR':
            print('ASSIGN -> ID := EXPR')
            ret = self.inter_rep.find_by_name(self.props_stack[-3].identifier)
            print(ret, self.props_stack[-3])
            if ret[2] == 0:
                print('给常量赋值')
                exit(-1)
            else:
                if ret[0] > 1:
                    print('乱花渐欲迷人眼，浅草才能没马蹄')
                    exit(-1)
                self.logWriter.write('STO', ret[0], ret[1][1])
            self.props_stack = self.props_stack[:-3]
        elif cmd == 'ITEM -> ITEM MUL_DIV FACTOR':
            print('ITEM -> ITEM MUL_DIV FACTOR')
            if self.props_stack[-2].token_type == TokenType.TIMES:
                self.logWriter.write('OPR', 0, 4)
            elif self.props_stack[-2].token_type == TokenType.DIVIDE:
                self.logWriter.write('OPR', 0, 5)
            else:
                print('* / 符号错误')
                exit(-1)
            self.props_stack = self.props_stack[:-2]

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
            self.props_stack.append(tk)

        elif cmd[0] == 'r':
            # print(self.parser.G_indexed[int(cmd[1:])])
            tp = self.parser.G_indexed[int(cmd[1:])][1]  # A -> B, tp = B
            lp = self.parser.G_indexed[int(cmd[1:])][0]
            # print(lp, "".join(tp))
            self.process_inter_rep(lp + " -> " + " ".join(tp))

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
    s = Syntax("../PL0_code/PL0_code0.in", open("./grammar.g").read())
    s.process()
    print(s.inter_rep)

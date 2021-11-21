from LR_table import SLRParser
from LR1_table import LR1Parser
from lexer import Lexer
from Grammar import Grammar
from myutils import Token, TokenType
from InterRep import InterRep
from LogWriter import LogWriter


class Syntax:
    def __init__(self, code_path: str, inter_path: str, grammar: str, parser_set='LR1'):

        self.inter_rep = InterRep()  # 用于生成中间代码
        self.inter_rep.add_procedure("_global", 0)
        self.logWriter = LogWriter(inter_path)
        self.lexer = Lexer(code_path, "")
        self.grammar = Grammar(grammar)
        # self.parser = LR1Parser(self.grammar)
        self.global_address_counter = 0  # 记录生成的地址
        # self.parser = SLRParser(self.grammar)
        if parser_set == 'LR1':
            self.parser = LR1Parser(self.grammar)
        else:
            self.parser = SLRParser(self.grammar)
        # print(self.parser.G_indexed)
        self.parsing_table = self.parser.parse_table
        self.state_stack = [0]  # type: list[int]
        self.readable_stack = []  # type: list[str]
        self.props_stack = []  # type: list[Token] # 存放各种属性
        # self.inter_rep
        # print(self.parser.parse_table)
        # for x in self.parser.parse_table.keys():
        #     print(x, self.parser.parse_table[x])

    # def subprocess_add_procedure
    def print_symbol_table(self):
        for x in self.inter_rep.procedure_dict.keys():
            p = self.inter_rep.procedure_dict[x]
            for y in p.const_dict.keys():
                print('NAME: {}\tKIND: CONSTANT\tVAL: {}\t'.format(y, p.const_dict[y]))
            for y in p.var_dict.keys():
                print('NAME: {}\tKIND: VARIABLE\tLEVEL: {}\tADR: {}'.format(y, p.level, p.var_dict[y][1]))
            chi = [self.inter_rep.procedure_dict[x] for x in self.inter_rep.procedure_dict.keys() if
                   self.inter_rep.procedure_dict[x].father == p.name]
            for y in chi:
                print('NAME: {}\tKIND: PROCEDURE\tLEVEL: {}\tADR: {}'.format(y.name, y.level, y.address))
            # print(chi)

    def check_props_stack(self, token_types: list) -> bool:
        if len(self.props_stack) < len(token_types):
            print('panic in check props_stack')
            exit(-1)
        for (i, x) in enumerate(token_types):
            if self.props_stack[-(len(token_types) - i)].token_type != x:
                print('panic in check props_stack')
                exit(-1)
        return False

    def process_const_related(self, cmd: str):
        if cmd == 'CONST -> CONST_ ;':
            print('CONST -> CONST_ ;')
            self.props_stack = self.props_stack[:-2]

        elif cmd == 'CONST -> ^':
            print('CONST -> CONST_ ;')

        elif cmd == 'CONST_ -> const CONST_DEF':
            print('CONST_ -> const CONST_DEF')
            self.props_stack = self.props_stack[:-1]

        elif cmd == 'CONST_ -> CONST_ , CONST_DEF':
            print('CONST_ -> CONST_ , CONST_DEF')
            self.props_stack = self.props_stack[:-2]

        elif cmd == 'CONST_DEF -> ID = UINT':
            print('CONST_DEF -> ID = UINT')
            self.check_props_stack([TokenType.IDENTIFIER, TokenType.EQUAL, TokenType.NUMBER])
            # print(self.props_stack)
            self.inter_rep.add_const(self.props_stack[-3].identifier, self.props_stack[-1].number)
            self.props_stack = self.props_stack[:-2]

    def process_var_related(self, cmd: str):
        if cmd == 'VARIABLE -> VARIABLE_ ;':
            self.props_stack = self.props_stack[:-2]
        elif cmd == 'VARIABLE -> ^':
            print('VARIABLE -> ^')
        elif cmd == 'VARIABLE_ -> var ID':
            print('VARIABLE_ -> var ID')
            self.check_props_stack([TokenType.VAR, TokenType.IDENTIFIER])
            self.inter_rep.add_var(self.props_stack[-1].identifier)
            # print('add', self.props_stack[-1].identifier)
            self.props_stack = self.props_stack[: -1]
            # print(self.props_stack)
        elif cmd == 'VARIABLE_ -> VARIABLE_ , ID':
            # print('VARIABLE_ -> VARIABLE_ , ID')
            self.check_props_stack([TokenType.COMMA, TokenType.IDENTIFIER])
            self.inter_rep.add_var(self.props_stack[-1].identifier)
            # print('add', self.props_stack[-1].identifier)
            self.props_stack = self.props_stack[: -2]
        # print("*********\n", self.inter_rep)

    def process_procedure_related(self, cmd: str):
        if cmd == 'PROCEDURE -> PROCEDURE_':
            print('PROCEDURE -> PROCEDURE_')

        elif cmd == 'PROCEDURE -> ^':
            print('PROCEDURE -> ^')

        elif cmd == 'PROCEDURE_ -> PROCEDURE_ PROC_HEAD SUBPROG ;':
            print('PROCEDURE_ -> PROCEDURE_ PROC_HEAD SUBPROG ;')
            self.props_stack = self.props_stack[:-1]

        elif cmd == 'PROCEDURE_ -> PROC_HEAD SUBPROG ;':
            print('PROCEDURE_ -> PROC_HEAD SUBPROG ;')
            self.props_stack = self.props_stack[:-1]

        elif cmd == "PROC_HEAD -> procedure ID ;":
            print("PROC_HEAD -> procedure ID ;")
            self.check_props_stack([TokenType.PROCEDURE, TokenType.IDENTIFIER, TokenType.SEMICOLON])
            self.inter_rep.add_procedure(self.props_stack[-2].identifier, self.inter_rep.current_procedure.level + 1)
            self.props_stack = self.props_stack[: -3]
            # print(self.props_stack)

    def process_assign_related(self, cmd: str):
        if cmd == 'ASSIGN -> ID := EXPR':
            print('ASSIGN -> ID := EXPR')
            ret = self.inter_rep.find_by_name(self.props_stack[-3].identifier)
            if ret[2] == 0:
                print('给常量赋值')
                exit(-1)
            else:
                if ret[0] > 1:
                    print('乱花渐欲迷人眼，浅草才能没马蹄')
                    exit(-1)
                self.logWriter.write('STO', ret[0], ret[1][1])
            self.props_stack = self.props_stack[:-3]

    def process_comp_related(self, cmd: str):
        if cmd == 'COMP -> COMP_BEGIN end':
            print('COMP -> COMP_BEGIN end')
            self.props_stack = self.props_stack[:-1]

        elif cmd == 'COMP_BEGIN -> begin STATEMENT':
            print('COMP_BEGIN -> begin STATEMENT')
            self.props_stack = self.props_stack[:-1]

        elif cmd == 'COMP_BEGIN -> COMP_BEGIN ; STATEMENT':
            print('COMP_BEGIN -> COMP_BEGIN ; STATEMENT')
            self.props_stack = self.props_stack[:-1]

    def process_factor_related(self, cmd: str):
        if cmd == 'FACTOR -> ID':
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

    def process_expr_related(self, cmd: str):
        if cmd == 'EXPR -> EXPR PLUS_MINUS ITEM':
            print('EXPR -> EXPR PLUS_MINUS ITEM')
            # print(s)
            print(self.props_stack)
            if self.props_stack[-2].token_type == TokenType.MINUS:
                self.logWriter.write('OPR', 0, 3)
            else:
                self.logWriter.write('OPR', 0, 2)
            self.props_stack = self.props_stack[:-2]

        elif cmd == 'EXPR -> PLUS_MINUS ITEM':
            print('EXPR -> PLUS_MINUS ITEM')
            print(self.props_stack[-2])
            if self.props_stack[-2].token_type == TokenType.MINUS:
                self.logWriter.write('OPR', 0, 1)
            self.props_stack = self.props_stack[:-1]
        elif cmd == 'EXPR -> ITEM':
            print('EXPR -> ITEM')

    def process_item_related(self, cmd: str):
        if cmd == 'ITEM -> FACTOR':
            print("ITEM -> FACTOR")

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

    def process_call_related(self, cmd: str):
        if cmd == 'CALL -> call ID':
            print('CALL -> call ID')
            # self.props_stack[-1].identifier
            tmp_p = self.inter_rep.current_procedure
            while True:
                # 得到 tmp_p 的 儿子们
                ps = [self.inter_rep.procedure_dict[x] for x in self.inter_rep.procedure_dict.keys() if
                      self.inter_rep.procedure_dict[x].father == tmp_p.name]
                nps = [x for x in ps if x.name == self.props_stack[-1].identifier]
                if len(nps) == 0:
                    if tmp_p.father == "":
                        print('无中生有 调用了不存在的procedure')
                        exit(-1)
                    tmp_p = self.inter_rep.procedure_dict[tmp_p.father]
                else:
                    nps = nps[0]
                    self.logWriter.write('call', self.inter_rep.current_procedure.level + 1 - nps.level, nps.address)
                    break
            self.props_stack = self.props_stack[:-2]

    def process_read_related(self, cmd: str):
        if cmd == 'READ -> READ_BEGIN )':
            print('READ -> READ_BEGIN )')
            self.props_stack = self.props_stack[:-1]
        elif cmd == 'READ_BEGIN -> read ( ID':
            print('READ_BEGIN -> read ( ID')
            self.logWriter.write('OPR', 0, 16)

            ret = self.inter_rep.find_by_name(self.props_stack[-1].identifier)
            if ret[2] == 0:
                print('给常量赋值')
                exit(-1)
            else:
                if ret[0] > 1:
                    print('乱花渐欲迷人眼，浅草才能没马蹄')
                    exit(-1)
                self.logWriter.write('STO', ret[0], ret[1][1])

            self.props_stack = self.props_stack[:-3]

        elif cmd == 'READ_BEGIN -> READ_BEGIN , ID':
            print('READ_BEGIN -> READ_BEGIN , ID')
            self.logWriter.write('OPR', 0, 16)

            ret = self.inter_rep.find_by_name(self.props_stack[-1].identifier)
            if ret[2] == 0:
                print('给常量赋值')
                exit(-1)
            else:
                if ret[0] > 1:
                    print('乱花渐欲迷人眼，浅草才能没马蹄')
                    exit(-1)
                self.logWriter.write('STO', ret[0], ret[1][1])

            self.props_stack = self.props_stack[:-2]

    def process_write_related(self, cmd: str):
        if cmd == 'WRITE -> WRITE_BEGIN )':
            print('WRITE -> WRITE_BEGIN )')
            self.props_stack = self.props_stack[:-1]

        elif cmd == 'WRITE_BEGIN -> write ( ID':
            print('WRITE_BEGIN -> write ( ID')
            ret = self.inter_rep.find_by_name(self.props_stack[-1].identifier)
            if ret is None:
                print('找不到对应标识符')
                exit(-1)
            if ret[2] == 0:
                self.logWriter.write('LIT', ret[0], ret[1])
                self.logWriter.write('OPR', 0, 14)
            else:
                self.logWriter.write('LOD', ret[0], ret[1][1])
                self.logWriter.write('OPR', 0, 14)
            self.props_stack = self.props_stack[:-3]

        elif cmd == 'WRITE_BEGIN -> WRITE_BEGIN , ID':
            print('WRITE_BEGIN -> WRITE_BEGIN , ID')
            ret = self.inter_rep.find_by_name(self.props_stack[-1].identifier)
            if ret is None:
                print('找不到对应标识符')
                exit(-1)
            if ret[2] == 0:
                self.logWriter.write('LIT', ret[0], ret[1])
                self.logWriter.write('OPR', 0, 14)
            else:
                self.logWriter.write('LOD', ret[0], ret[1][1])
                self.logWriter.write('OPR', 0, 14)
            self.props_stack = self.props_stack[:-2]

    def process_cond_related(self, cmd: str):
        if cmd == 'COND -> if CONDITION then M_COND STATEMENT':
            print('COND -> if CONDITION then M_COND STATEMENT')
            ret = self.props_stack[-1]
            # print('abab', ret)
            self.logWriter.cmd_arr[ret.number - 1].num = self.logWriter.total_line
            # self.logWriter.write('last -1 is', self.logWriter.total_line)
            self.props_stack = self.props_stack[:-4]
        elif cmd == 'M_COND -> ^':
            print('M_COND -> ^')
            self.logWriter.write('JPC', 0, self.logWriter.total_line + 2)
            self.logWriter.write('JMP', 0, -1)
            self.props_stack.append(Token(TokenType.NUMBER, 'jmp', self.logWriter.total_line))
        elif cmd == 'CONDITION -> EXPR REL EXPR':
            print('CONDITION -> EXPR REL EXPR')
            if self.props_stack[-2].token_type == TokenType.EQUAL:
                self.logWriter.write('OPR', 0, 8)
            elif self.props_stack[-2].token_type == TokenType.NEQUAL:
                self.logWriter.write('OPR', 0, 9)
            elif self.props_stack[-2].token_type == TokenType.LESS:
                self.logWriter.write('OPR', 0, 10)
            elif self.props_stack[-2].token_type == TokenType.LESS_OR_EQUAL:
                self.logWriter.write('OPR', 0, 13)
            elif self.props_stack[-2].token_type == TokenType.GREATER:
                self.logWriter.write('OPR', 0, 12)
            elif self.props_stack[-2].token_type == TokenType.GREATER_OR_EQUAL:
                self.logWriter.write('OPR', 0, 11)
            self.props_stack = self.props_stack[:-2]

        elif cmd == 'CONDITION -> odd EXPR':
            print('CONDITION -> odd EXPR')
            self.logWriter.write('OPR', 0, 6)
            self.props_stack = self.props_stack[:-1]

    def process_while_related(self, cmd: str):
        if cmd == 'WHILE -> while M_WHILE_FORE CONDITION do M_WHILE_TAIL STATEMENT':
            print('WHILE -> while M_WHILE_FORE CONDITION do M_WHILE_TAIL STATEMENT')
            self.logWriter.write('JMP', 0, self.props_stack[-4].number)
            self.logWriter.cmd_arr[self.props_stack[-1].number - 1].num = self.logWriter.total_line
            self.props_stack = self.props_stack[:-5]

        elif cmd == 'M_WHILE_FORE -> ^':
            print('M_WHILE_FORE -> ^')
            self.props_stack.append(Token(TokenType.NUMBER, 'while_head', self.logWriter.total_line))

        elif cmd == 'M_WHILE_TAIL -> ^':
            print('M_WHILE_TAIL -> ^')
            self.logWriter.write('JPC', 0, self.logWriter.total_line + 2)
            self.logWriter.write('JMP', 0, -1)
            self.props_stack.append(Token(TokenType.NUMBER, 'while_tail jmp', self.logWriter.total_line))

        # self.props_stack.append(Token(TokenType.NUMBER, 'while', self.logWriter.total_line-1))

    def process_inter_rep(self, cmd: str):
        print(cmd, self.props_stack)
        # print(cmd)
        if cmd in ['CONST -> CONST_ ;',
                   'CONST -> ^',
                   'CONST_ -> const CONST_DEF',
                   'CONST_ -> CONST_ , CONST_DEF',
                   'CONST_DEF -> ID = UINT']:
            self.process_const_related(cmd)

        elif cmd in ['VARIABLE -> VARIABLE_ ;',
                     'VARIABLE -> ^',
                     'VARIABLE_ -> var ID',
                     'VARIABLE_ -> VARIABLE_ , ID']:
            self.process_var_related(cmd)

        elif cmd in ['PROCEDURE -> PROCEDURE_',
                     'PROCEDURE -> ^',
                     'PROCEDURE_ -> PROCEDURE_ PROC_HEAD SUBPROG ;',
                     'PROCEDURE_ -> PROC_HEAD SUBPROG ;',
                     'PROC_HEAD -> procedure ID ;']:
            self.process_procedure_related(cmd)

        elif cmd in ['ASSIGN -> ID := EXPR']:
            self.process_assign_related(cmd)

        elif cmd in ['COMP -> COMP_BEGIN end',
                     'COMP_BEGIN -> begin STATEMENT',
                     'COMP_BEGIN -> COMP_BEGIN ; STATEMENT']:
            self.process_comp_related(cmd)

        elif cmd in ['FACTOR -> ID',
                     'FACTOR -> UINT',
                     'FACTOR -> ( EXPR )']:
            self.process_factor_related(cmd)

        elif cmd in ['ITEM -> FACTOR',
                     'ITEM -> ITEM MUL_DIV FACTOR']:
            self.process_item_related(cmd)

        elif cmd in ['EXPR -> PLUS_MINUS ITEM',
                     'EXPR -> EXPR PLUS_MINUS ITEM',
                     'EXPR -> ITEM']:
            self.process_expr_related(cmd)

        elif cmd in ['CALL -> call ID']:
            self.process_call_related(cmd)

        elif cmd in ['READ -> READ_BEGIN )',
                     'READ_BEGIN -> read ( ID',
                     'READ_BEGIN -> READ_BEGIN , ID']:
            self.process_read_related(cmd)

        elif cmd in ['WRITE -> WRITE_BEGIN )',
                     'WRITE_BEGIN -> write ( ID',
                     'WRITE_BEGIN -> WRITE_BEGIN , ID']:
            self.process_write_related(cmd)

        elif cmd in ['COND -> if CONDITION then M_COND STATEMENT',
                     'M_COND -> ^',
                     'CONDITION -> EXPR REL EXPR',
                     'CONDITION -> odd EXPR']:
            self.process_cond_related(cmd)

        elif cmd in ['WHILE -> while M_WHILE_FORE CONDITION do M_WHILE_TAIL STATEMENT',
                     'M_WHILE_FORE -> ^',
                     'M_WHILE_TAIL -> ^']:
            self.process_while_related(cmd)

        elif cmd == 'SUBPROG -> CONST VARIABLE PROCEDURE M_STATEMENT STATEMENT':
            print('SUBPROG -> CONST VARIABLE PROCEDURE M_STATEMENT STATEMENT')
            if self.inter_rep.current_procedure.father != "":
                self.inter_rep.current_procedure = self.inter_rep.procedure_dict[
                    self.inter_rep.current_procedure.father]
            self.logWriter.write('OPR', 0, 0)
            # print(self.props_stack)
        elif cmd == 'M_STATEMENT -> ^':
            print('M_STATEMENT -> ^')
            volumn = 3 + len(self.inter_rep.current_procedure.var_dict)
            self.inter_rep.current_procedure.address = self.logWriter.total_line
            # self.logWriter.write('')
            self.logWriter.write('int', 0, volumn)

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
        self.logWriter.write('JMP', 0, -1)
        while self.lexer.has_next():
            t = self.lexer.get_next()
            if t.token_type is None:
                break
            # print('lexer', t.token_type, t.number, t.identifier)
            self.process_one_hop(t.token_type.value, t)

            # cmd = parsing_table[state_stack[-1]][t.token_type.value]
        self.logWriter.cmd_arr[0].num = self.inter_rep.procedure_dict['_global'].address

    def iprocess(self):
        while True:
            t = input()
            self.process_one_hop(t, None)


if __name__ == '__main__':
    s = Syntax("../PL0_code/PL0_code3.in", 'abab.txt', open("./grammar.g").read())
    s.process()
    s.logWriter.flush()
    print("")
    s.print_symbol_table()
    # print(s.inter_rep)

#!/usr/bin/env python3

# from graphviz import Digraph
from Grammar import Grammar
import argparse
import json


def first_follow(G):
    def union(set_1, set_2):
        set_1_len = len(set_1)
        set_1 |= set_2

        return set_1_len != len(set_1)

    first = {symbol: set() for symbol in G.symbols}
    first.update((terminal, {terminal}) for terminal in G.terminals)  # first terminal 加入
    follow = {symbol: set() for symbol in G.nonterminals}
    follow[G.start].add('$')

    while True:
        updated = False

        for head, bodies in G.grammar.items():
            for body in bodies:
                for symbol in body:
                    if symbol != '^':
                        updated |= union(first[head], first[symbol] - set('^'))

                        if '^' not in first[symbol]:
                            break
                    else:
                        updated |= union(first[head], set('^'))
                else:
                    updated |= union(first[head], set('^'))

                aux = follow[head]
                for symbol in reversed(body):
                    if symbol == '^':
                        continue
                    if symbol in follow:
                        updated |= union(follow[symbol], aux - set('^'))
                    if '^' in first[symbol]:
                        aux = aux | first[symbol]
                    else:
                        aux = first[symbol]

        if not updated:
            return first, follow


class LR1Parser:
    def __init__(self, G):
        self.G_prime = Grammar(f"{G.start}' -> {G.start}\n{G.grammar_str}")  # 扩展文法
        # print(f"{G.start}' -> {G.start}\n{G.grammar_str}")
        self.max_G_prime_len = len(max(self.G_prime.grammar, key=len))  # 这是啥？
        # print(self.max_G_prime_len)
        self.G_indexed = []

        for head, bodies in self.G_prime.grammar.items():
            for body in bodies:
                self.G_indexed.append([head, body])

        self.first, self.follow = first_follow(self.G_prime)
        # self.LR1_items(self.G_prime)
        # exit(0)
        self.C = self.LR1_items(self.G_prime)

        self.action = list(self.G_prime.terminals) + ['$']
        self.goto = list(self.G_prime.nonterminals - {self.G_prime.start})
        print(self.first)
        self.parse_table_symbols = self.action + self.goto
        self.parse_table = self.LR1_construct_table()

    def construct_follow(self, s: tuple, extra: str) -> set:
        # print('new', s)
        ret = set()
        flag = True
        for x in s:
            # print(x, self.first[x])
            ret = ret | self.first[x]
            if '^' in self.first[x]:
                flag = False
                break
        ret.discard('^')
        if flag:
            ret = ret | {extra}
        # print(ret, extra)
        # if 'v' in ret:
        #     exit(1)
        return ret

    def LR1_CLOSURE(self, dict_of_trans: dict) -> dict:
        ret = dict_of_trans
        # (): {()}
        while True:
            item_len = len(ret)
            for head, bodies in dict_of_trans.copy().items():
                for body in bodies.copy():
                    if '.' in body[:-1]:
                        symbol_after_dot = body[body.index('.') + 1]
                        if symbol_after_dot in self.G_prime.nonterminals:
                            symbol_need_first_loc = body.index('.') + 2
                            if symbol_need_first_loc == len(body):
                                # A -> ... .B
                                for G_body in self.G_prime.grammar[symbol_after_dot]:
                                    ret.setdefault((symbol_after_dot, head[1]), set()).add(
                                        ('.',) if G_body == ('^',) else ('.',) + G_body
                                    )
                            else:
                                # A -> ... .BC
                                for j in self.construct_follow(body[symbol_need_first_loc:], head[1]):
                                    for G_body in self.G_prime.grammar[symbol_after_dot]:
                                        ret.setdefault((symbol_after_dot, j), set()).add(
                                            ('.',) if G_body == ('^',) else ('.',) + G_body
                                        )
            if item_len == len(ret):
                break
        return ret

    def LR1_GOTO(self, state: dict, c: str) -> dict:
        goto = {}
        for head, bodies in state.items():
            for body in bodies:
                if '.' in body[:-1]:
                    dot_pos = body.index('.')
                    if body[dot_pos + 1] == c:
                        replaced_dot_body = body[:dot_pos] + (c, '.') + body[dot_pos + 2:]
                        for C_head, C_bodies in self.LR1_CLOSURE({head: {replaced_dot_body}}).items():
                            # print(got)
                            goto.setdefault(C_head, set()).update(C_bodies)
        # print(goto)
        return goto

    def LR1_items(self, G_prime):
        C = [self.LR1_CLOSURE({(G_prime.start, '$'): {('.', G_prime.start[:-1])}})]

        while True:
            item_len = len(C)

            for I in C.copy():
                for X in G_prime.symbols:
                    goto = self.LR1_GOTO(I, X)
                    # if len(goto) != 0:
                    #     print(goto)
                    if goto and goto not in C:
                        C.append(goto)

            if item_len == len(C):
                # print(C)
                return C

    def LR1_construct_table(self):
        parse_table = {r: {c: '' for c in self.parse_table_symbols} for r in range(len(self.C))}
        # print(self.parse_table_symbols)
        for i, I in enumerate(self.C):
            # print(I)
            for head, bodies in I.items():
                # print(head, bodies)
                for body in bodies:
                    if '.' in body[:-1]:  # CASE 2 a
                        symbol_after_dot = body[body.index('.') + 1]

                        if symbol_after_dot in self.G_prime.terminals:
                            s = f's{self.C.index(self.LR1_GOTO(I, symbol_after_dot))}'

                            if s not in parse_table[i][symbol_after_dot]:
                                if 'r' in parse_table[i][symbol_after_dot]:
                                    parse_table[i][symbol_after_dot] += '/'

                                parse_table[i][symbol_after_dot] += s

                    elif body[-1] == '.' and head[0] != self.G_prime.start:  # CASE 2 b
                        for j, (G_head, G_body) in enumerate(self.G_indexed):
                            if G_head == head[0] and (G_body == body[:-1] or G_body == ('^',) and body == ('.',)):
                                # for f in self.follow[head]:
                                #     if parse_table[i][f]:
                                #         parse_table[i][f] += '/'
                                #
                                #     parse_table[i][f] += f'r{j}'
                                # print(head[1],'!')
                                if parse_table[i][head[1]]:
                                    parse_table[i][head[1]] += '/'
                                parse_table[i][head[1]] += f'r{j}'
                                break

                    else:  # CASE 2 c
                        # print('here')
                        parse_table[i]['$'] = 'acc'

            for A in self.G_prime.nonterminals:  # CASE 3
                j = self.LR1_GOTO(I, A)

                if j in self.C:
                    parse_table[i][A] = self.C.index(j)

        return parse_table

    def print_info(self):
        print(self.action)

        print(self.goto)

        # print(self.parse_table)

        print(json.dumps(self.parse_table, indent=4))

        def fprint(text, variable):
            print(f'{text:>12}: {", ".join(variable)}')

        # def print_line():
        #     print(f'+{("-" * width + "+") * (len(list(self.G_prime.symbols) + ["$"]))}')
        #
        # def symbols_width(symbols):
        #     return (width + 1) * len(symbols) - 1

        print('AUGMENTED GRAMMAR:')

        for i, (head, body) in enumerate(self.G_indexed):
            print(f'{i:>{len(str(len(self.G_indexed) - 1))}}: {head:>{self.max_G_prime_len}} -> {" ".join(body)}')

        print()
        fprint('TERMINALS', self.G_prime.terminals)
        fprint('NONTERMINALS', self.G_prime.nonterminals)
        fprint('SYMBOLS', self.G_prime.symbols)


def main():
    # parser = argparse.ArgumentParser()
    # parser.add_argument('grammar_file', type=argparse.FileType('r'), help='text file to be used as grammar')
    # parser.add_argument('-g', action='store_true', help='generate automaton')
    # parser.add_argument('tokens', help='tokens to be parsed - all tokens are separated with spaces')
    # args = parser.parse_args()
    file = "grammar.g"

    G = Grammar(open(file).read())
    slr_parser = LR1Parser(G)
    slr_parser.print_info()
    # results = slr_parser.LR_parser(args.tokens)
    # slr_parser.print_LR_parser(results)

    # if args.g:
    #     slr_parser.generate_automaton()


if __name__ == "__main__":
    main()

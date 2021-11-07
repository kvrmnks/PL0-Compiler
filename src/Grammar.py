file_path = "grammar.g"

grammar_file = open(file_path, "r")


class Grammar:
    def __init__(self, grammar_str):
        # print(grammar_str.splitlines())
        self.grammar_str = '\r'.join(filter(None, grammar_str.splitlines()))
        self.grammar = {}
        self.start = None
        self.terminals = set()
        self.nonterminals = set()

        for production in list(filter(None, grammar_str.splitlines())):
            head, _, bodies = production.partition(' -> ') # head 箭头前部
            # print(bodies)
            if not head.isupper():
                raise ValueError \
                    (f'\'{head} -> {bodies}\': Head \'{head}\' is not capitalized to be treated as a nonterminal.')

            if not self.start:
                self.start = head # 第一个出现的为 'S'

            self.grammar.setdefault(head, set())
            self.nonterminals.add(head)
            # print(bodies)
            bodies = {tuple(body.split()) for body in ' '.join(bodies.split()).split('|')}
            # print(bodies) # 每个生成式 是 一个 tuple

            for body in bodies:
                if '^' in body and body != ('^',):  # 这是为啥呀
                    raise ValueError(f'\'{head} -> {" ".join(body)}\': Null symbol \'^\' is not allowed here.')

                self.grammar[head].add(body)

                for symbol in body:
                    if not symbol.isupper() and symbol != '^':
                        self.terminals.add(symbol)
                    elif symbol.isupper():
                        self.nonterminals.add(symbol)

        self.symbols = self.terminals | self.nonterminals


g = Grammar(grammar_file.read())

# Grammar.terminals

# print(g.terminals)

# print(g.grammar)

# print(g.start)

# print(grammar_file.read())

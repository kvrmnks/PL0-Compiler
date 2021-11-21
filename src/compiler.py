from syntax import *

source_code_path = '../PL0_code/PL0_code3.in'
obj_file_path = 'abab.txt'
grammar_file_path = './grammar.g'


def compiler():
    syn = Syntax(source_code_path, obj_file_path, open(grammar_file_path).read(), 'LR1')
    syn.process()
    syn.logWriter.flush()
    print("")
    syn.print_symbol_table()


if __name__ == "__main__":
    compiler()

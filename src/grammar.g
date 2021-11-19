PROG -> SUBPROG

SUBPROG -> CONST VARIABLE PROCEDURE M_STATEMENT STATEMENT

M_STATEMENT -> ^ @ down

CONST -> CONST_ ; @ down remain 0
CONST -> ^ @ down remain 0
CONST_ -> const CONST_DEF @ done remain 1
CONST_ -> CONST_ , CONST_DEF @ done remain 1
CONST_DEF -> ID = UINT @ down remain 1

UINT -> num @ down auto remain 1

VARIABLE -> VARIABLE_ ; @ down remain 0
VARIABLE -> ^ @ down remain 0
VARIABLE_ -> var ID @ down remain 1
VARIABLE_ -> VARIABLE_ , ID @ down remain 1

ID -> id @ down auto remain 1

PROCEDURE -> PROCEDURE_ @ down remain 0
PROCEDURE -> ^ @ down remain 0
PROCEDURE_ -> PROCEDURE_ PROC_HEAD SUBPROG ; @ down remain 0
PROCEDURE_ -> PROC_HEAD SUBPROG ; @ down remain 0      assume subproc remain 0
PROC_HEAD -> procedure ID ; @ down remain 0

STATEMENT -> ASSIGN
STATEMENT -> COND
STATEMENT -> WHILE
STATEMENT -> CALL
STATEMENT -> READ
STATEMENT -> WRITE
STATEMENT -> COMP
STATEMENT -> ^

ASSIGN -> ID := EXPR @ down remain 0

COMP -> COMP_BEGIN end  @down remain 0
COMP_BEGIN -> begin STATEMENT @ down remain 0
COMP_BEGIN -> COMP_BEGIN ; STATEMENT @ down remain 0

COND -> if CONDITION then M_COND STATEMENT @down remain 0
M_COND -> ^ @ down append 1
CONDITION -> EXPR REL EXPR @ down remain 1
CONDITION -> odd EXPR @ down remain 1

EXPR -> PLUS_MINUS ITEM @ down remain 1
EXPR -> EXPR PLUS_MINUS ITEM @down remain 1
EXPR -> ITEM @ down auto remain 1

ITEM -> FACTOR @ down auto remain 1
ITEM -> ITEM MUL_DIV FACTOR @down remain 1

FACTOR -> ID @ down remain 1
FACTOR -> UINT @ down auto remain 1
FACTOR -> ( EXPR ) @down remain 1

PLUS_MINUS -> + @ down auto remain 1
PLUS_MINUS -> - @ down auto remain 1
MUL_DIV -> * @ down auto remain 1
MUL_DIV -> / @ down auto remain 1
REL -> = @ down auto remain 1
REL -> # @ down auto remain 1
REL -> < @ down auto remain 1
REL -> <= @ down auto remain 1
REL -> > @ down auto remain 1
REL -> >= @ down auto remain 1

CALL -> call ID @ down remain 0

WHILE -> while M_WHILE_FORE CONDITION do M_WHILE_TAIL STATEMENT @down remain 0
M_WHILE_FORE -> ^ @ down append 1
M_WHILE_TAIL -> ^ @ down append 1

READ -> READ_BEGIN ) @ down remain 0
READ_BEGIN -> read ( ID @ down remain 0
READ_BEGIN -> READ_BEGIN , ID @ down remain 0

WRITE -> WRITE_BEGIN ) @down remain 0
WRITE_BEGIN -> write ( ID @down remain 0
WRITE_BEGIN -> WRITE_BEGIN , ID @down remain 0

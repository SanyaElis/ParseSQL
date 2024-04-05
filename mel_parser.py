from lark import Lark, Transformer
from mel_ast import *

parser = Lark('''
    %import common.NUMBER
    %import common.CNAME
    %import common.NEWLINE
    %import common.WS

    %ignore WS

    COMMENT: "/*" /(.|\\n|\\r)+/ "*/"
        |  "//" /(.)+/ NEWLINE
    %ignore COMMENT

    num: NUMBER
    ident: CNAME | STRING | ALL
    STRING: /'[^']*'/
    
    ADD:     "+"
    SUB:     "-"
    MUL:     "*"
    DIV:     "/"
    AND:     "and"i
    OR:      "or"i
    BIT_AND: "&"
    BIT_OR:  "|"
    GE:      ">="
    LE:      "<="
    NEQ:     "<>"
    EQ:      "="
    GT:      ">"
    LT:      "<"
    ALL:     "*"
    
    call: ident "(" ( expr ( "," expr )* )? ")"

    ?group: num
        | ident
        | call
        | "(" add ")"

    ?mult: group
        | mult MUL group    -> binary
        | mult DIV group    -> binary

    ?add: mult
        | add ADD mult     -> binary
        | add SUB mult     -> binary
        
    ?compare: add
        | add GT add       -> binary
        | add GE add       -> binary
        | add LT add       -> binary
        | add LE add       -> binary
        | add EQ add       -> binary
        | add NEQ add      -> binary
        
    ?logical_and: compare
        | logical_and AND compare  -> binary
    
    ?logical_or: logical_and
        | logical_or OR logical_and  -> binary

    ?expr: logical_or
    
    expr_list: expr ("," expr)*
        
    ?table: ident
    ?as_expr: expr
        | expr "as"i? ident | "(" select ")" "as"i? ident
    
    as_expr_list: as_expr ("," as_expr)*  -> expr_list
        
    ?join: table
    
    empty_expr:  -> empty
    empty_expr_list:  -> expr_list
    
    ?where: "where"i expr -> where_clause 
        | empty_expr
        
    ?group_by: "group"i "by"i expr_list -> group_clause
        | empty_expr_list
        
    ?having: "having"i expr -> having_clause
        | empty_expr
        
    ?order_by: "order"i "by"i expr_list -> order_clause
        | empty_expr_list
    
    select: "select"i as_expr_list "from"i join where group_by having order_by

    ?start: select
''', start="start")


class MelASTBuilder(Transformer):
    def _call_userfunc(self, tree, new_children=None):
        # Assumes tree is already transformed
        children = new_children if new_children is not None else tree.children
        try:
            f = getattr(self, tree.data)
        except AttributeError:
            return self.__default__(tree.data, children, tree.meta)
        else:
            return f(*children)

    def __getattr__(self, item):
        if isinstance(item, str) and item.upper() == item:
            return lambda x: x

        if item in ('true', 'empty'):
            return lambda: NumNode(1)
        if item in ('binary',):
            def get_bin_op_node(*args):
                op = BinOp(args[1].value.lower())  # todo check lover()
                return BinOpNode(op, args[0], args[2])

            return get_bin_op_node
        else:
            def get_node(*args):
                cls = eval(''.join(x.capitalize() or '_' for x in item.split('_')) + 'Node')
                return cls(*args)

            return get_node


def parse(prog: str) -> ExprNode:
    prog = parser.parse(str(prog))
    print(prog.pretty())
    prog = MelASTBuilder().transform(prog)
    return prog

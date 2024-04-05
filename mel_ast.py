from abc import ABC, abstractmethod
from typing import Callable, Tuple, Union, Optional
from enum import Enum


class AstNode(ABC):
    @property
    def childs(self) -> Tuple['AstNode', ...]:
        return ()

    @abstractmethod
    def __str__(self) -> str:
        pass

    @property
    def tree(self) -> [str, ...]:
        res = [str(self)]
        childs = self.childs
        for i, child in enumerate(childs):
            ch0, ch = '├', '│'
            if i == len(childs) - 1:
                ch0, ch = '└', ' '
            res.extend(((ch0 if j == 0 else ch) + ' ' + s for j, s in enumerate(child.tree)))
        return res

    def visit(self, func: Callable[['AstNode'], None]) -> None:
        func(self)
        map(func, self.childs)

    def __getitem__(self, index):
        return self.childs[index] if index < len(self.childs) else None


class ExprNode(AstNode):
    pass


class ValueNode(ExprNode):
    pass


class NumNode(ValueNode):
    def __init__(self, num: float):
        super().__init__()
        self.num = float(num)

    def __str__(self) -> str:
        return str(self.num)


class IdentNode(ValueNode):
    def __init__(self, name: str):
        super().__init__()
        self.name = str(name)

    def __str__(self) -> str:
        return str(self.name)


class BinOp(Enum):
    ADD = '+'
    SUB = '-'
    MUL = '*'
    DIV = '/'
    GT = '>'
    GE = '>='
    LT = '<'
    LE = '<='
    EQ = '='
    NEQ = '<>'
    AND = 'and'
    OR = 'or'


class BinOpNode(ExprNode):
    def __init__(self, op: BinOp, arg1: ValueNode, arg2: ValueNode):
        super().__init__()
        self.op = op
        self.arg1 = arg1
        self.arg2 = arg2

    @property
    def childs(self) -> Tuple[ValueNode, ValueNode]:
        return self.arg1, self.arg2

    def __str__(self) -> str:
        return str(self.op.value)


class AsExprNode(ExprNode):
    def __init__(self, expr: ExprNode, name: IdentNode):
        super().__init__()
        self.expr = expr
        self.name = name

    @property
    def childs(self) -> Tuple[ExprNode]:
        return self.expr,

    def __str__(self) -> str:
        return f'as {self.name}'


class ExprListNode(AstNode):
    def __init__(self, *exprs: ExprNode):
        super().__init__()
        self.exprs = exprs

    @property
    def childs(self) -> Tuple[ValueNode, ValueNode]:
        return self.exprs

    def __str__(self) -> str:
        return '...'


class WhereClauseNode(AstNode):
    def __init__(self, *exprs: ExprNode):
        super().__init__()
        self.exprs = exprs

    @property
    def childs(self) -> Tuple[ValueNode, ValueNode]:
        return self.exprs

    def __str__(self) -> str:
        return 'where'


class GroupClauseNode(AstNode):
    def __init__(self, *exprs: ExprNode):
        super().__init__()
        self.exprs = exprs

    @property
    def childs(self) -> Tuple[ValueNode, ValueNode]:
        return self.exprs

    def __str__(self) -> str:
        return 'group by'


class HavingClauseNode(AstNode):
    def __init__(self, *exprs: ExprNode):
        super().__init__()
        self.exprs = exprs

    @property
    def childs(self) -> Tuple[ValueNode, ValueNode]:
        return self.exprs

    def __str__(self) -> str:
        return 'having'


class OrderClauseNode(AstNode):
    def __init__(self, *exprs: ExprNode):
        super().__init__()
        self.exprs = exprs

    @property
    def childs(self) -> Tuple[ValueNode, ValueNode]:
        return self.exprs

    def __str__(self) -> str:
        return 'order by'


class SelectNode(AstNode):
    def __init__(self, selects: ExprListNode, tables: IdentNode, where: WhereClauseNode,
                 group_by: GroupClauseNode, having: HavingClauseNode, order_by: OrderClauseNode):
        super().__init__()
        self.selects = selects
        self.tables = tables
        self.where = where
        self.group_by = group_by
        self.having = having
        self.order_by = order_by

    @property
    def childs(self) -> Tuple[ValueNode, ValueNode]:
        return self.selects, self.tables, self.where, self.group_by, self.having, self.order_by

    def __str__(self) -> str:
        return 'select'

from __future__ import annotations

from abc import ABC, abstractmethod
from plox.scan import Token


class Visitor(ABC):
    @abstractmethod
    def visitBinaryExpr(expr: Binary):
        pass

    @abstractmethod
    def visitGroupingExpr(expr: Grouping):
        pass

    @abstractmethod
    def visitLiteralExpr(expr: Literal):
        pass

    @abstractmethod
    def visitUnaryExpr(expr: Unary):
        pass


class Expr(ABC):
    pass
    @abstractmethod
    def accept(self, visitor: Visitor):
        pass


class Binary(Expr):

    def __init__(self, left: Expr, operator: Token, right: Expr) -> None:
        self.left: Expr = left
        self.operator: Token = operator
        self.right: Expr = right
    def accept(self, visitor: Visitor):
        return visitor.visitBinaryExpr(self)


class Grouping(Expr):

    def __init__(self, expression: Expr) -> None:
        self.expression: Expr = expression
    def accept(self, visitor: Visitor):
        return visitor.visitGroupingExpr(self)


class Literal(Expr):

    def __init__(self, value: object) -> None:
        self.value: object = value
    def accept(self, visitor: Visitor):
        return visitor.visitLiteralExpr(self)


class Unary(Expr):

    def __init__(self, operator: Token, right: Expr) -> None:
        self.operator: Token = operator
        self.right: Expr = right
    def accept(self, visitor: Visitor):
        return visitor.visitUnaryExpr(self)



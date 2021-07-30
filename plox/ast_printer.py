from plox.ast import (
    Visitor,
    Binary,
    Grouping,
    Literal,
    Unary,
    Expr
)
from plox.scan import Token, TokenType

class ASTPrinter(Visitor):

    def print(self, expr: Expr):
        return expr.accept(self)

    def visitBinaryExpr(self, expr: Binary):
        return self.parenthesise(
            expr.operator.lexeme,
            expr.left,
            expr.right
        )

    def visitGroupingExpr(self, expr: Grouping):
        return self.parenthesise("group", expr.expression)

    def visitLiteralExpr(self, expr: Literal):
        if expr.value is None:
            return "nil"
        return str(expr.value)

    def visitUnaryExpr(self, expr: Unary):
        return self.parenthesise(
            expr.operator.lexeme,
            expr.right
        )

    def parenthesise(self, name: str, *exprs: tuple):
        build = f"({name}"
        for expr in exprs:
            build += f" {expr.accept(self)}"
        build += ")"
        return build

def main():
    expression = Binary(
        Unary(
            Token(TokenType.MINUS, "-", None, 1),
            Literal(123),
        ),
        Token(TokenType.STAR, "*", None, 1),
        Grouping(Literal(45.67))
    )
    print(ASTPrinter().print(expression))

if __name__ == "__main__":
    main()
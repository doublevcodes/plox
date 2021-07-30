from enum import auto, Enum
from string import ascii_letters
import sys
from pathlib import Path

class TokenType(Enum):
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    COMMA = auto()
    DOT = auto()
    MINUS = auto()
    PLUS = auto()
    SEMICOLON = auto()
    SLASH = auto()
    STAR = auto()

    NOT = auto()
    NOT_EQUAL = auto()
    EQUAL = auto()
    EQUAL_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()

    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()

    AND = auto()
    CLASS = auto()
    ELSE = auto()
    FALSE = auto()
    FUN = auto()
    FOR = auto()
    IF = auto()
    NIL = auto()
    OR = auto()
    PRINT = auto()
    RETURN = auto()
    SUPER = auto()
    THIS = auto()
    TRUE = auto()
    VAR = auto()
    WHILE = auto()

    EOF = auto()


class Token:
    
    def __init__(self, type_: TokenType, lexeme: str, literal: object, line: int) -> None:
        self.type = type_
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self) -> str:
        return f"{self.type.name.ljust(15)} | {self.lexeme.ljust(10)} | {self.literal}"

class Scanner:

    keywords: dict[str, TokenType] = {
        "and": TokenType.AND,
        "class": TokenType.CLASS,
        "else": TokenType.ELSE,
        "false": TokenType.FALSE,
        "for": TokenType.FOR,
        "fun": TokenType.FUN,
        "if": TokenType.IF,
        "nil": TokenType.NIL,
        "or": TokenType.OR,
        "print": TokenType.PRINT,
        "return": TokenType.RETURN,
        "super": TokenType.SUPER,
        "this": TokenType.THIS,
        "var": TokenType.VAR,
        "while": TokenType.WHILE
    }
    
    def __init__(self, source: str) -> None:
        self.source: str = source
        self.tokens: list[Token] = []
        self.start = 0
        self.current = 0
        self.line = 1

    def scan_tokens(self) -> list[Token]:
        
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens
    
    def scan_token(self):
        c: str = self.advance()
        if c  == "(":
            self._add_token(TokenType.LEFT_PAREN)
        elif c == ")":
            self._add_token(TokenType.RIGHT_PAREN)
        elif c == "{":
            self._add_token(TokenType.LEFT_BRACE)
        elif c == "}":
            self._add_token(TokenType.RIGHT_BRACE)
        elif c == ",":
            self._add_token(TokenType.COMMA)
        elif c == ".":
            self._add_token(TokenType.DOT)
        elif c == "-":
            self._add_token(TokenType.MINUS)
        elif c == "+":
            self._add_token(TokenType.PLUS)
        elif c == ";":
            self._add_token(TokenType.SEMICOLON)
        elif c == "*":
            self._add_token(TokenType.STAR)
        elif c == "!":
            self._add_token(TokenType.NOT_EQUAL if self.match("=") else TokenType.NOT)
        elif c == "=":
            self._add_token(TokenType.EQUAL_EQUAL if self.match("=") else TokenType.EQUAL)
        elif c == "<":
            self._add_token(TokenType.LESS_EQUAL if self.match("=") else TokenType.LESS)
        elif c == ">":
            self._add_token(TokenType.GREATER_EQUAL if self.match("=") else TokenType.GREATER)
        elif c == "/":
            if self.match("/"):
                while self.peek() != "\n" and not self.is_at_end():
                    self.advance()
            elif self.match("*"):
                while self.peek() != "*" and self.peek_next() != "/" and not self.is_at_end():
                    if self.peek() == "\n":
                        self.line += 1
                    self.advance()
                self.advance()
                self.advance()
            else:
                self._add_token(TokenType.SLASH)
        elif c in (" ", "\r", "\t"):
            pass
        elif c == "\n":
            self.line += 1
        elif c == "\"":
            self.string()
        elif c.isdigit():
            self.number()
        elif c in (ascii_letters + "_"):
            self.identifier()
        else:
            error(self.line, f"Unexpected character {c}")

    def advance(self):
        next_ = self.source[self.current]
        self.current += 1
        return next_
    
    def match(self, expected: str):
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    def peek(self) -> str:
        if self.is_at_end():
            return "\0"
        return self.source[self.current]
    
    def peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def string(self):
        while self.peek() != "\"" and not self.is_at_end():
            if self.peek() == "\n":
                self.line += 1
            self.advance()
        
        if self.is_at_end():
            error(self.line, "Unterminated string")
        
        self.advance()

        value = self.source[self.start + 1:self.current - 1]
        self.add_token(TokenType.STRING, value)
        
    def number(self):
        while self.peek().isdigit():
            self.advance()
        
        if self.peek() == "." and self.peek_next().isdigit():
            self.advance()
            while self.peek().isdigit():
                self.advance()
        self.add_token(TokenType.NUMBER, self.source[self.start:self.current])

    def identifier(self):
        while self.peek().isalnum():
            self.advance()
        text: str = self.source[self.start:self.current]
        type_: TokenType = Scanner.keywords.get(text, TokenType.IDENTIFIER)
        self._add_token(type_)

    def _add_token(self, type: TokenType):
        self.add_token(type, None)

    def add_token(self, type: TokenType, literal: object):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

class Lox:

    had_error: bool = False

def report(line: int, where: str, message: str):
    print(f"Line {line} | Error{where}: {message}")

def error(line: int, message: str):
    report(line, "", message)
    Lox.had_error = True

def run(source: str):
    scanner: Scanner = Scanner(source)
    tokens: list[Token] = scanner.scan_tokens()

    for token in tokens:
        print(token)

def run_file(path: str):
    path: Path = Path(path)

    if not path.exists():
        print(f"{path} does not exist")
        sys.exit(66)

    with open(path, "r") as code:
        source: str = code.read()
    run(source)
    if Lox.had_error:
        sys.exit(65)

def run_prompt():
    while True:
        print("> ", end="")
        line = input()
        if line == "exit":
            break
        run(line)
        Lox.had_error = False

def main(*args: tuple[str]):
    if len(args) > 1:
        print("Usage: plox [script]")
        sys.exit(64)
    elif len(args) == 1:
        run_file(args[0])
    else:
        run_prompt()
    
if __name__ == "__main__":
    main(*(sys.argv[1:]))
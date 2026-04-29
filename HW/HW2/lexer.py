from enum import Enum, auto
from dataclasses import dataclass
from typing import Optional

class TokenType(Enum):
    VAR = auto()
    FUNC = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    FOR = auto()
    BREAK = auto()
    CONTINUE = auto()
    RETURN = auto()
    INT = auto()
    FLOAT = auto()
    BOOL = auto()
    STRING = auto()
    ARRAY = auto()
    VOID = auto()
    IDENT = auto()
    INT_LITERAL = auto()
    FLOAT_LITERAL = auto()
    STRING_LITERAL = auto()
    BOOL_LITERAL = auto()
    PLUS = auto()
    MINUS = auto()
    MUL = auto()
    DIV = auto()
    MOD = auto()
    EQ = auto()
    NEQ = auto()
    LT = auto()
    GT = auto()
    LE = auto()
    GE = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    ASSIGN = auto()
    COLON = auto()
    ARROW = auto()
    COMMA = auto()
    LPAREN = auto()
    RPAREN = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    LBRACE = auto()
    RBRACE = auto()
    SEMICOLON = auto()
    EOF = auto()

@dataclass
class Token:
    type: TokenType
    value: any
    line: int
    column: int

class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.current_char = source[0] if source else None

    def advance(self):
        if self.current_char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1

        self.pos += 1
        self.current_char = self.source[self.pos] if self.pos < len(self.source) else None

    def peek(self, offset: int = 1) -> Optional[str]:
        peek_pos = self.pos + offset
        return self.source[peek_pos] if peek_pos < len(self.source) else None

    def skip_whitespace(self):
        while self.current_char and self.current_char in ' \t\n\r':
            self.advance()

    def skip_comment(self):
        if self.current_char == '/':
            if self.peek() == '/':
                while self.current_char and self.current_char != '\n':
                    self.advance()

    def read_identifier(self) -> str:
        result = ''
        while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        return result

    def read_number(self) -> tuple:
        result = ''
        is_float = False

        while self.current_char and (self.current_char.isdigit() or self.current_char == '.'):
            if self.current_char == '.':
                if is_float:
                    break
                is_float = True
            result += self.current_char
            self.advance()

        if is_float:
            return (float(result), TokenType.FLOAT_LITERAL)
        else:
            return (int(result), TokenType.INT_LITERAL)

    def read_string(self) -> str:
        self.advance()
        result = ''
        while self.current_char and self.current_char != '"':
            if self.current_char == '\\':
                self.advance()
                if self.current_char == 'n':
                    result += '\n'
                elif self.current_char == 't':
                    result += '\t'
                elif self.current_char == '\\':
                    result += '\\'
                elif self.current_char == '"':
                    result += '"'
                else:
                    result += self.current_char
            else:
                result += self.current_char
            self.advance()
        self.advance()
        return result

    def get_keyword(self, ident: str) -> TokenType:
        keywords = {
            'var': TokenType.VAR,
            'func': TokenType.FUNC,
            'if': TokenType.IF,
            'else': TokenType.ELSE,
            'while': TokenType.WHILE,
            'for': TokenType.FOR,
            'break': TokenType.BREAK,
            'continue': TokenType.CONTINUE,
            'return': TokenType.RETURN,
            'int': TokenType.INT,
            'float': TokenType.FLOAT,
            'bool': TokenType.BOOL,
            'string': TokenType.STRING,
            'array': TokenType.ARRAY,
            'void': TokenType.VOID,
            'true': TokenType.BOOL_LITERAL,
            'false': TokenType.BOOL_LITERAL,
        }
        return keywords.get(ident, TokenType.IDENT)

    def tokenize(self) -> list[Token]:
        tokens = []

        while self.current_char:
            self.skip_whitespace()
            self.skip_comment()
            self.skip_whitespace()

            if not self.current_char:
                break

            line = self.line
            column = self.column

            if self.current_char.isalpha() or self.current_char == '_':
                ident = self.read_identifier()
                token_type = self.get_keyword(ident)
                value = ident if token_type == TokenType.IDENT else (ident == 'true')
                tokens.append(Token(token_type, value, line, column))

            elif self.current_char.isdigit():
                value, token_type = self.read_number()
                tokens.append(Token(token_type, value, line, column))

            elif self.current_char == '"':
                value = self.read_string()
                tokens.append(Token(TokenType.STRING_LITERAL, value, line, column))

            elif self.current_char == '+':
                self.advance()
                tokens.append(Token(TokenType.PLUS, '+', line, column))
            elif self.current_char == '-':
                self.advance()
                if self.current_char == '>':
                    self.advance()
                    tokens.append(Token(TokenType.ARROW, '->', line, column))
                else:
                    tokens.append(Token(TokenType.MINUS, '-', line, column))
            elif self.current_char == '*':
                self.advance()
                tokens.append(Token(TokenType.MUL, '*', line, column))
            elif self.current_char == '/':
                self.advance()
                tokens.append(Token(TokenType.DIV, '/', line, column))
            elif self.current_char == '%':
                self.advance()
                tokens.append(Token(TokenType.MOD, '%', line, column))

            elif self.current_char == '=':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    tokens.append(Token(TokenType.EQ, '==', line, column))
                else:
                    tokens.append(Token(TokenType.ASSIGN, '=', line, column))
            elif self.current_char == '!':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    tokens.append(Token(TokenType.NEQ, '!=', line, column))
                else:
                    tokens.append(Token(TokenType.NOT, '!', line, column))
            elif self.current_char == '<':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    tokens.append(Token(TokenType.LE, '<=', line, column))
                else:
                    tokens.append(Token(TokenType.LT, '<', line, column))
            elif self.current_char == '>':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    tokens.append(Token(TokenType.GE, '>=', line, column))
                else:
                    tokens.append(Token(TokenType.GT, '>', line, column))

            elif self.current_char == '&':
                self.advance()
                if self.current_char == '&':
                    self.advance()
                    tokens.append(Token(TokenType.AND, '&&', line, column))
            elif self.current_char == '|':
                self.advance()
                if self.current_char == '|':
                    self.advance()
                    tokens.append(Token(TokenType.OR, '||', line, column))

            elif self.current_char == ':':
                self.advance()
                tokens.append(Token(TokenType.COLON, ':', line, column))
            elif self.current_char == ',':
                self.advance()
                tokens.append(Token(TokenType.COMMA, ',', line, column))
            elif self.current_char == '(':
                self.advance()
                tokens.append(Token(TokenType.LPAREN, '(', line, column))
            elif self.current_char == ')':
                self.advance()
                tokens.append(Token(TokenType.RPAREN, ')', line, column))
            elif self.current_char == '[':
                self.advance()
                tokens.append(Token(TokenType.LBRACKET, '[', line, column))
            elif self.current_char == ']':
                self.advance()
                tokens.append(Token(TokenType.RBRACKET, ']', line, column))
            elif self.current_char == '{':
                self.advance()
                tokens.append(Token(TokenType.LBRACE, '{', line, column))
            elif self.current_char == '}':
                self.advance()
                tokens.append(Token(TokenType.RBRACE, '}', line, column))
            elif self.current_char == ';':
                self.advance()
                tokens.append(Token(TokenType.SEMICOLON, ';', line, column))

            else:
                raise ValueError(f"Unknown character '{self.current_char}' at line {self.line}, column {self.column}")

        tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return tokens

def lex(source: str) -> list[Token]:
    return Lexer(source).tokenize()

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            source = f.read()
        tokens = lex(source)
        for token in tokens:
            print(f"{token.type.name:20} {repr(token.value):20} L{token.line}:C{token.column}")
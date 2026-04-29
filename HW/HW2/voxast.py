from dataclasses import dataclass
from typing import Optional, List
from lexer import Token, TokenType

@dataclass
class ASTNode:
    pass

@dataclass
class Program(ASTNode):
    statements: List[ASTNode]

@dataclass
class Type(ASTNode):
    name: str

@dataclass
class VariableDecl(ASTNode):
    name: str
    var_type: Type
    value: ASTNode

@dataclass
class FunctionDecl(ASTNode):
    name: str
    params: List[tuple[str, Type]]
    return_type: Type
    body: 'Block'

@dataclass
class Block(ASTNode):
    statements: List[ASTNode]

@dataclass
class IfStatement(ASTNode):
    condition: ASTNode
    then_branch: Block
    else_branch: Optional[Block]

@dataclass
class WhileStatement(ASTNode):
    condition: ASTNode
    body: Block

@dataclass
class ForStatement(ASTNode):
    init: VariableDecl
    condition: ASTNode
    update: ASTNode
    body: Block

@dataclass
class BreakStatement(ASTNode):
    pass

@dataclass
class ContinueStatement(ASTNode):
    pass

@dataclass
class ReturnStatement(ASTNode):
    value: Optional[ASTNode]

@dataclass
class ExpressionStatement(ASTNode):
    expression: ASTNode

@dataclass
class BinaryOp(ASTNode):
    operator: str
    left: ASTNode
    right: ASTNode

@dataclass
class UnaryOp(ASTNode):
    operator: str
    operand: ASTNode

@dataclass
class CallExpr(ASTNode):
    name: str
    arguments: List[ASTNode]

@dataclass
class ArrayAccess(ASTNode):
    name: str
    index: ASTNode

@dataclass
class Identifier(ASTNode):
    name: str

@dataclass
class Literal(ASTNode):
    value: any
    literal_type: str

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def current(self) -> Token:
        return self.tokens[self.pos]

    def advance(self):
        self.pos += 1

    def expect(self, token_type: TokenType) -> Token:
        if self.current().type != token_type:
            raise ValueError(f"Expected {token_type}, got {self.current().type} at L{self.current().line}")
        token = self.current()
        self.advance()
        return token

    def parse(self) -> Program:
        statements = []
        while self.current().type != TokenType.EOF:
            statements.append(self.statement())
        return Program(statements)

    def statement(self) -> ASTNode:
        token = self.current()

        if token.type == TokenType.VAR:
            return self.variable_decl()
        elif token.type == TokenType.FUNC:
            return self.function_decl()
        elif token.type == TokenType.IF:
            return self.if_statement()
        elif token.type == TokenType.WHILE:
            return self.while_statement()
        elif token.type == TokenType.FOR:
            return self.for_statement()
        elif token.type == TokenType.BREAK:
            self.advance()
            self.expect(TokenType.SEMICOLON)
            return BreakStatement()
        elif token.type == TokenType.CONTINUE:
            self.advance()
            self.expect(TokenType.SEMICOLON)
            return ContinueStatement()
        elif token.type == TokenType.RETURN:
            return self.return_statement()
        elif token.type == TokenType.LBRACE:
            return self.block()
        elif token.type == TokenType.SEMICOLON:
            self.advance()
            return ExpressionStatement(Literal(None, 'void'))
        else:
            expr = self.expression()
            self.expect(TokenType.SEMICOLON)
            return ExpressionStatement(expr)

    def variable_decl(self) -> VariableDecl:
        self.expect(TokenType.VAR)
        name = self.expect(TokenType.IDENT).value
        self.expect(TokenType.COLON)
        var_type = self.type_()
        self.expect(TokenType.ASSIGN)
        value = self.expression()
        self.expect(TokenType.SEMICOLON)
        return VariableDecl(name, var_type, value)

    def type_(self) -> Type:
        token = self.current()
        if token.type in [TokenType.INT, TokenType.FLOAT, TokenType.BOOL, TokenType.STRING, TokenType.ARRAY, TokenType.VOID]:
            self.advance()
            return Type(token.value)
        raise ValueError(f"Unknown type: {token.type}")

    def function_decl(self) -> FunctionDecl:
        self.expect(TokenType.FUNC)
        name = self.expect(TokenType.IDENT).value
        self.expect(TokenType.LPAREN)

        params = []
        if self.current().type != TokenType.RPAREN:
            while True:
                param_name = self.expect(TokenType.IDENT).value
                self.expect(TokenType.COLON)
                param_type = self.type_()
                params.append((param_name, param_type))
                if self.current().type == TokenType.COMMA:
                    self.advance()
                else:
                    break

        self.expect(TokenType.RPAREN)
        self.expect(TokenType.ARROW)
        return_type = self.type_()
        body = self.block()
        return FunctionDecl(name, params, return_type, body)

    def block(self) -> Block:
        self.expect(TokenType.LBRACE)
        statements = []
        while self.current().type != TokenType.RBRACE:
            statements.append(self.statement())
        self.expect(TokenType.RBRACE)
        return Block(statements)

    def if_statement(self) -> IfStatement:
        self.expect(TokenType.IF)
        self.expect(TokenType.LPAREN)
        condition = self.expression()
        self.expect(TokenType.RPAREN)
        then_branch = self.block()

        else_branch = None
        if self.current().type == TokenType.ELSE:
            self.advance()
            else_branch = self.block()

        return IfStatement(condition, then_branch, else_branch)

    def while_statement(self) -> WhileStatement:
        self.expect(TokenType.WHILE)
        self.expect(TokenType.LPAREN)
        condition = self.expression()
        self.expect(TokenType.RPAREN)
        body = self.block()
        return WhileStatement(condition, body)

    def for_statement(self) -> ForStatement:
        self.expect(TokenType.FOR)
        self.expect(TokenType.LPAREN)
        init = self.variable_decl()
        condition = self.expression()
        self.expect(TokenType.SEMICOLON)
        update = self.expression()
        self.expect(TokenType.RPAREN)
        body = self.block()
        return ForStatement(init, condition, update, body)

    def return_statement(self) -> ReturnStatement:
        self.expect(TokenType.RETURN)
        if self.current().type == TokenType.SEMICOLON:
            self.advance()
            return ReturnStatement(None)
        value = self.expression()
        self.expect(TokenType.SEMICOLON)
        return ReturnStatement(value)

    def expression(self) -> ASTNode:
        return self.assignment_expr()

    def assignment_expr(self) -> ASTNode:
        left = self.logical_or_expr()
        if self.current().type == TokenType.ASSIGN:
            self.advance()
            right = self.expression()
            return BinaryOp('=', left, right)
        return left

    def logical_or_expr(self) -> ASTNode:
        left = self.logical_and_expr()
        while self.current().type == TokenType.OR:
            op = self.current().value
            self.advance()
            right = self.logical_and_expr()
            left = BinaryOp(op, left, right)
        return left

    def logical_and_expr(self) -> ASTNode:
        left = self.equality_expr()
        while self.current().type == TokenType.AND:
            op = self.current().value
            self.advance()
            right = self.equality_expr()
            left = BinaryOp(op, left, right)
        return left

    def equality_expr(self) -> ASTNode:
        left = self.relational_expr()
        while self.current().type in [TokenType.EQ, TokenType.NEQ]:
            op = self.current().value
            self.advance()
            right = self.relational_expr()
            left = BinaryOp(op, left, right)
        return left

    def relational_expr(self) -> ASTNode:
        left = self.additive_expr()
        while self.current().type in [TokenType.LT, TokenType.GT, TokenType.LE, TokenType.GE]:
            op = self.current().value
            self.advance()
            right = self.additive_expr()
            left = BinaryOp(op, left, right)
        return left

    def additive_expr(self) -> ASTNode:
        left = self.multiplicative_expr()
        while self.current().type in [TokenType.PLUS, TokenType.MINUS]:
            op = self.current().value
            self.advance()
            right = self.multiplicative_expr()
            left = BinaryOp(op, left, right)
        return left

    def multiplicative_expr(self) -> ASTNode:
        left = self.unary_expr()
        while self.current().type in [TokenType.MUL, TokenType.DIV, TokenType.MOD]:
            op = self.current().value
            self.advance()
            right = self.unary_expr()
            left = BinaryOp(op, left, right)
        return left

    def unary_expr(self) -> ASTNode:
        if self.current().type in [TokenType.PLUS, TokenType.MINUS, TokenType.NOT]:
            op = self.current().value
            self.advance()
            operand = self.unary_expr()
            return UnaryOp(op, operand)
        return self.call_expr()

    def call_expr(self) -> ASTNode:
        primary = self.primary_expr()

        if self.current().type == TokenType.LPAREN:
            self.advance()
            args = []
            if self.current().type != TokenType.RPAREN:
                while True:
                    args.append(self.expression())
                    if self.current().type == TokenType.COMMA:
                        self.advance()
                    else:
                        break
            self.expect(TokenType.RPAREN)
            return CallExpr(primary.name if isinstance(primary, Identifier) else '', args)

        if self.current().type == TokenType.LBRACKET:
            self.advance()
            index = self.expression()
            self.expect(TokenType.RBRACKET)
            if isinstance(primary, Identifier):
                return ArrayAccess(primary.name, index)
            raise ValueError("Invalid array access")

        return primary

    def primary_expr(self) -> ASTNode:
        token = self.current()

        if token.type == TokenType.IDENT:
            self.advance()
            return Identifier(token.value)

        if token.type == TokenType.INT_LITERAL:
            self.advance()
            return Literal(token.value, 'int')

        if token.type == TokenType.FLOAT_LITERAL:
            self.advance()
            return Literal(token.value, 'float')

        if token.type == TokenType.STRING_LITERAL:
            self.advance()
            return Literal(token.value, 'string')

        if token.type == TokenType.BOOL_LITERAL:
            self.advance()
            return Literal(token.value, 'bool')

        if token.type == TokenType.LBRACKET:
            return self.array_literal()

        if token.type == TokenType.LPAREN:
            self.advance()
            expr = self.expression()
            self.expect(TokenType.RPAREN)
            return expr

        raise ValueError(f"Unexpected token: {token.type}")

    def array_literal(self) -> ASTNode:
        self.expect(TokenType.LBRACKET)
        elements = []
        if self.current().type != TokenType.RBRACKET:
            while True:
                elements.append(self.expression())
                if self.current().type == TokenType.COMMA:
                    self.advance()
                else:
                    break
        self.expect(TokenType.RBRACKET)
        return Literal(elements, 'array')

def parse(tokens: List[Token]) -> Program:
    return Parser(tokens).parse()
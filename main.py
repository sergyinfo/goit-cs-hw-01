"""
Example of simple interpreter for arithmetic expressions.
Supports +, -, *, /, (, ) operators.

Example:
    1 + 2 * 3
    (1 + 2) * 3
    1 + 2 * 3 - 4 / 2
    1 + (2 * 3) - 4 / 2
"""

class LexicalError(Exception):
    """Exception for lexical errors."""
    pass

class ParsingError(Exception):
    """Exception for parsing errors."""
    pass

class TokenType:
    """Token types."""
    INTEGER = "INTEGER"
    PLUS = "PLUS"
    MINUS = "MINUS"
    MUL = "MUL"
    DIV = "DIV"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    EOF = "EOF"

class Token:
    """
    Token class.

    Attributes:
        type (TokenType): Type of token.
        value (int, str): Value of token

    Methods:
        __str__: Returns string representation of token.
    """
    def __init__(self, type, value):
        """
        Initializes token with type and value.

        Args:
            type (TokenType): Type of token.
            value (int, str): Value of token.
        """
        self.type = type
        self.value = value

    def __str__(self):
        """
        Returns string representation of token.
        """
        return f"Token({self.type}, {repr(self.value)})"

class Lexer:
    """
    Lexer class.

    Attributes:
        text (str): Text to tokenize.
        pos (int): Current position in text.
        current_char (str): Current character in text.

    Methods:
        advance: Moves to the next character in text.
        skip_whitespace: Skips whitespaces in text.
        integer: Returns integer from text.
        get_next_token: Returns next token from text.

    Raises:
        LexicalError: If unknown character in text.
    """
    def __init__(self, text):
        """
        Initializes lexer with text.

        Args:
            text (str): Text to tokenize.

        Attributes:
            text (str): Text to tokenize.
            pos (int): Current position in text.
            current_char (str): Current character in text.
        """
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def advance(self):
        """
        Moves to the next character in text.
        If end of text, sets current_char to None.
        """
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        """
        Skips whitespaces in text.
        Moves to the next character in text until not whitespace.
        """
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        """
        Returns integer from text.

        Returns:
            int: Integer from text.
            
        Raises:
            LexicalError: If unknown character in text.
        """
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        """
        Returns next token from text.

        Returns:
            Token: Next token from text.

        Raises:
            LexicalError: If unknown character in text.
        """
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(TokenType.INTEGER, self.integer())

            if self.current_char == '+':
                self.advance()
                return Token(TokenType.PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(TokenType.MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(TokenType.MUL, '*')

            if self.current_char == '/':
                self.advance()
                return Token(TokenType.DIV, '/')

            if self.current_char == '(':
                self.advance()
                return Token(TokenType.LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(TokenType.RPAREN, ')')

            raise LexicalError("Невідомий символ: " + self.current_char)

        return Token(TokenType.EOF, None)

class AST:
    """
    Abstract syntax tree class.

    Methods:
        __str__: Returns string representation of AST.

    Raises:
        Exception: If method not implemented.
    """
    pass

class BinOp(AST):
    """
    Binary operation class.

    Attributes:
        left (AST): Left node.
        op (Token): Operator node.
        right (AST): Right node.

    Methods:
        __str__: Returns string representation of binary operation.
        
    Raises:
        Exception: If method not implemented.
    """
    def __init__(self, left, op, right):
        """
        Initializes binary operation with left, operator and right nodes.

        Args:
            left (AST): Left node.
            op (Token): Operator node.
            right (AST): Right node.

        Attributes:
            left (AST): Left node.
            op (Token): Operator node.
            right (AST): Right node.

        Raises:
            Exception: If method not implemented.
        """
        self.left = left
        self.op = op
        self.right = right

class Num(AST):
    """
    Number class.

    Attributes:
        token (Token): Token node.
        value (int): Value of number.

    Methods:
        __str__: Returns string representation of number.

    Raises:
        Exception: If method not implemented.
    """
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Parser:
    """
    Parser class.

    Attributes:
        lexer (Lexer): Lexer object.
        current_token (Token): Current token.

    Methods:
        error: Raises parsing error.
        eat: Consumes token if matches token type.
        factor: Parses factor.
        term: Parses term.
        expr: Parses expression.

    Raises:
        ParsingError: If parsing error.
    """
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        """
        Raises parsing error.

        Raises:
            ParsingError: Parsing error.
        """
        raise ParsingError("Помилка синтаксичного аналізу")

    def eat(self, token_type):
        """
        Consumes token if matches token type.

        Args:
            token_type (TokenType): Token type.

        Raises:
            ParsingError: If token type not matches.
        """
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        """
        Parses factor.

        Returns:
            AST: Factor node.

        Raises:
            ParsingError: If parsing error.
        """
        token = self.current_token
        if token.type == TokenType.INTEGER:
            self.eat(TokenType.INTEGER)
            return Num(token)
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
            return node

    def term(self):
        """
        Parses term.

        Returns:
            AST: Term node.

        Raises:
            ParsingError: If parsing error.
        """
        node = self.factor()
        while self.current_token.type in (TokenType.MUL, TokenType.DIV):
            token = self.current_token
            if token.type == TokenType.MUL:
                self.eat(TokenType.MUL)
            elif token.type == TokenType.DIV:
                self.eat(TokenType.DIV)

            node = BinOp(left=node, op=token, right=self.factor())

        return node

    def expr(self):
        """
        Parses expression.

        Returns:
            AST: Expression node.

        Raises:
            ParsingError: If parsing error.
        """
        node = self.term()
        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            if token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
            elif token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)

            node = BinOp(left=node, op=token, right=self.term())

        return node

class Interpreter:
    """
    Interpreter class.

    Attributes:
        parser (Parser): Parser object.

    Methods:
        visit_BinOp: Visits binary operation node.
        visit_Num: Visits number node.
        interpret: Interprets expression.
        visit: Visits node.
        generic_visit: Raises exception for not implemented method.

    Raises:
        Exception: If method not implemented
    """
    def __init__(self, parser):
        """
        Initializes interpreter with parser.

        Args:
            parser (Parser): Parser object.

        Attributes:
            parser (Parser): Parser object.

        Raises:
            Exception: If method not implemented.
        """
        self.parser = parser

    def visit_BinOp(self, node):
        """
        Visits binary operation node.

        Args:
            node (BinOp): Binary operation node.

        Returns:
            int: Result of binary operation.

        Raises:
            Exception: If operator not supported.
        """
        if node.op.type == TokenType.PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == TokenType.MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == TokenType.MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == TokenType.DIV:
            return self.visit(node.left) / self.visit(node.right)

    def visit_Num(self, node):
        """
        Visits number node.

        Args:
            node (Num): Number node.

        Returns:
            int: Value of number.

        Raises:
            Exception: If method not implemented.
        """
        return node.value

    def interpret(self):
        """
        Interprets expression.

        Returns:
            int: Result of expression.

        Raises:
            Exception: If method not implemented.
        """
        tree = self.parser.expr()
        return self.visit(tree)

    def visit(self, node):
        """
        Visits node.

        Args:
            node (AST): Node to visit.

        Returns:
            int: Result of node.

        Raises:
            Exception: If method not implemented.
        """
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f'Немає методу visit_{type(node).__name__}')

def main():
    """
    Main function for interpreter.
    Reads expression from input and interprets it.
    Supports exit command to exit from program.
    """
    while True:
        try:
            text = input('Введіть вираз (або "exit" для виходу): ')
            if text.lower() == 'exit':
                print("Вихід із програми.")
                break
            lexer = Lexer(text)
            parser = Parser(lexer)
            interpreter = Interpreter(parser)
            result = interpreter.interpret()
            print(f"Результат: {result}")
        except Exception as e:
            print(e)

if __name__ == "__main__":
    main()

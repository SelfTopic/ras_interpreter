from dataclasses import dataclass
from ._tokenizer import _Tokenizer

@dataclass
class WhileLoop:
    condition: str
    body: str

class WhileLoopTokenize(_Tokenizer):
    def __init__(self, code: str):
        super().__init__(code)

    def tokenize(self) -> WhileLoop:
        """Токенизирует цикл while."""
        self.skip_whitespace()

        if not self.code.startswith("whi"):
            raise SyntaxError("Expected 'whi' keyword")
        self.pos += len("whi")
        self.advance()
        self.skip_whitespace()

        condition = self._tokenize_condition()
        self.skip_whitespace()

        if self.code[self.pos:self.pos + 2] != "::":
            raise SyntaxError("Expected '::' before body")
        self.pos += 2
        self.advance()

        body = self._tokenize_body()
        self.skip_whitespace()

        if self.code[self.pos:self.pos + 2] != "::":
            raise SyntaxError("Expected '::' after body")
        self.pos += 2
        self.advance()

        return WhileLoop(condition=condition, body=body), self.pos

    def advance(self) -> None:
        self.pos += 1
        if self.pos < len(self.code):
            self.char = self.code[self.pos]
        else:
            self.char = ''

    def skip_whitespace(self):
        while self.char and self.char.isspace():
            self.advance()

    def _tokenize_condition(self) -> str:
        """Токенизирует условие цикла."""
        if self.char != ":":
            raise SyntaxError("Expected ':' before condition")
        self.advance()

        condition = ""
        while self.char != ":":
            if not self.char:
                raise SyntaxError("Expected ':' after condition")
            condition += self.char
            self.advance()
        self.advance()

        return condition

    def _tokenize_body(self) -> str:
        """Токенизирует тело цикла."""
        body = ""
        while self.char != '':
            if self.code[self.pos:self.pos + 2] == "::":
                return body
            body += self.char
            self.advance()
        return body

if __name__ == '__main__':
    code_example = "whi :true: :: print: \"Hello, World!\" # ::"
    tokenizer = WhileLoopTokenize(code_example)
    while_loop = tokenizer.tokenize()
    print(while_loop)

    code_example2 = "whi :var > 0: :: var << var - 1 # ::"
    tokenizer2 = WhileLoopTokenize(code_example2)
    while_loop2 = tokenizer2.tokenize()
    print(while_loop2)

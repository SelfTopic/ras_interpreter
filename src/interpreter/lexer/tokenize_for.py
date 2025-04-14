from dataclasses import dataclass
from typing import Any
from ._tokenizer import _Tokenizer

@dataclass
class ForLoop:
    variable_name: str
    iterable: Any  # Может быть имя переменной, массив, и т.д.
    body: str


class ForLoopTokenize(_Tokenizer):
    def __init__(self, code: str):
        super().__init__(code)

    def tokenize(self) -> ForLoop:
        """Токенизирует цикл for."""
        self.skip_whitespace()

        if not self.code.startswith("for"):
            raise SyntaxError("Expected 'for' keyword")
        self.pos += len("for")
        self.advance()
        self.skip_whitespace()

        variable_name = self._tokenize_variable_name()
        self.skip_whitespace()

        if self.code[self.pos:self.pos + 2] != "<<":
            raise SyntaxError("Expected '<<' after variable name")
        self.pos += 2
        self.advance()
        self.skip_whitespace()

        iterable = self._tokenize_iterable()
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

        return ForLoop(variable_name=variable_name, iterable=iterable, body=body), self.pos

    def _tokenize_variable_name(self) -> str:
        name = ""
        while self.char and (self.char.isalnum() or self.char == "_"):
            name += self.char
            self.advance()
        if not name:
            raise SyntaxError("Expected variable name")
        return name

    def _tokenize_iterable(self) -> Any:
        """Токенизирует итерируемый объект (пока только имя переменной)."""
        # TODO: Добавить поддержку массивов, диапазонов и т.д.
        name = ""
        while self.char and (self.char.isalnum() or self.char == "_"):
            name += self.char
            self.advance()
        if not name:
            raise SyntaxError("Expected iterable")
        return name

    def _tokenize_body(self) -> str:
         """Токенизирует тело цикла."""
         body = ""
         count_operators = 0

         while self.char != '':

            if self.code[self.pos:self.pos + 2] == "::":
                return body

            body += self.char
            self.advance()

         return body


if __name__ == '__main__':
    code_example = "for i << my_list :: print: i # ::"
    tokenizer = ForLoopTokenize(code_example)
    for_loop = tokenizer.tokenize()
    print(for_loop)

    code_example2 = f"""for index << array :: 
print: index #
local value :integer: << index # 
::"""
    tokenizer2 = ForLoopTokenize(code_example2)
    for_loop2 = tokenizer2.tokenize()
    print(for_loop2)
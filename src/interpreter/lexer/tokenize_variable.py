# ЧЕКНИ СТРОКИ 
# 108

from dataclasses import dataclass
from typing import Union, Any, List
from ._tokenizer import _Tokenizer
from .tokenize_value import ValueTokenize


@dataclass
class Variable:
    name: str
    value: Union[str, int, float, bool, None]  # Пример типов, можно расширить
    variable_types: List[str]
    is_local: bool
    is_global: bool


class VariableTokenize(_Tokenizer):
    def __init__(self, code: str):
        super().__init__(code)

    def tokenize(self):
        """Токенизирует объявление переменной (local или global)."""
        self.skip_whitespace()

        is_local = False
        is_global = False

        if self.code.startswith("local"):
            is_local = True
            self.pos += len("local")
        elif self.code.startswith("global"):
            is_global = True
            self.pos += len("global")
        else:
            raise SyntaxError("Expected 'local' or 'global'")

        self.advance() #пропускаем пробел

        name = self._tokenize_name()
        self.skip_whitespace()

        if self.char != ":":
            raise SyntaxError("Expected ':' after variable name")
        self.advance()

        variable_types = self._tokenize_type()
        self.skip_whitespace()

        if self.char != ":":
            raise SyntaxError("Expected ':' after variable type")
        self.advance()
        self.skip_whitespace()

        if self.code[self.pos:self.pos + 2] != "<<":

            # raise SyntaxError("Expected '<<' after ':'")
            self.pos += 2
            self.advance()
            self.skip_whitespace()

            value, offset = ValueTokenize(self.code[self.pos:], variable_types).tokenize()
            self.pos += offset
            self.char = self.code[self.pos]
        else:
            value = None
            # print(self.pos, self.)
            self.skip_whitespace()

        # if not value:
        #     raise ValueError()

        if self.char != "#":
            raise SyntaxError("Expected '#' at the end of variable declaration")
        #self.pos += 1 # consume the hash
        #self.advance()
        return Variable(name=name, value=value, variable_types=variable_types, is_local=is_local, is_global=is_global), self.pos

    def advance(self) -> None:
         self.pos += 1
         if self.pos < len(self.code):
             self.char = self.code[self.pos]
         else:
             self.char = ''

    def skip_whitespace(self):
        while self.char and self.char.isspace():
            self.advance()

    def _tokenize_name(self) -> str:
        name = ""
        while self.char and (self.char.isalnum() or self.char == "_"):
            name += self.char
            self.advance()
        if not name:
            raise SyntaxError("Expected variable name")
        return name

    def _tokenize_type(self) -> str:
        types = ""
        self.skip_whitespace()
        while (self.char and self.char.isalnum()) or self.char == "+":
            types += self.char
            self.advance()
            self.skip_whitespace()

        if not types:
            raise SyntaxError("Expected variable type")

        return types.split("++")


if __name__ == '__main__':
    code_example = "local my_var :integer: << 10 #"
    tokenizer = VariableTokenize(code_example)
    variable = tokenizer.tokenize()
    print(variable)

    code_example2 = "global pi :float: << 3.14 #"
    tokenizer2 = VariableTokenize(code_example2)
    variable2 = tokenizer2.tokenize()
    print(variable2)

    code_example3 = 'local message :string: << "Hello, world!" #'
    tokenizer3 = VariableTokenize(code_example3)
    variable3 = tokenizer3.tokenize()
    print(variable3)

    code_example4 = 'local is_valid :boolean: << true #'
    tokenizer4 = VariableTokenize(code_example4)
    variable4 = tokenizer4.tokenize()
    print(variable4)

    # Example with empty
    code_example5 = "local empty_var :empty: << #"
    tokenizer5 = VariableTokenize(code_example5)
    variable5 = tokenizer5.tokenize()
    print(variable5)


from dataclasses import dataclass
from typing import Union, Any


@dataclass
class Variable:
    name: str
    value: Union[str, int, float, bool, None]  # Пример типов, можно расширить
    variable_type: str
    is_local: bool
    is_global: bool


class VariableTokenize:

    def __init__(self, code: str):
        self.code = code
        self.pos = 0
        self.char = self.code[self.pos] if code else ''

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

        variable_type = self._tokenize_type()
        self.skip_whitespace()

        if self.char != ":":
            raise SyntaxError("Expected ':' after variable type")
        self.advance()
        self.skip_whitespace()

        if self.code[self.pos:self.pos + 2] != "<<":
            raise SyntaxError("Expected '<<' after ':'")
        self.pos += 2
        self.advance()
        self.skip_whitespace()

        value = self._tokenize_value(variable_type)
        self.skip_whitespace()

        if self.char != "#":
            raise SyntaxError("Expected '#' at the end of variable declaration")
        #self.pos += 1 # consume the hash
        #self.advance()
        return Variable(name=name, value=value, variable_type=variable_type, is_local=is_local, is_global=is_global), self.pos

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
        type_name = ""
        while self.char and self.char.isalnum():
            type_name += self.char
            self.advance()
        if not type_name:
            raise SyntaxError("Expected variable type")
        return type_name

    def _tokenize_value(self, variable_type: str) -> Union[str, int, float, bool, None]:
        """Токенизирует значение переменной в зависимости от типа."""
        if variable_type == "integer":
            return self._tokenize_integer()
        elif variable_type == "float":
            return self._tokenize_float()
        elif variable_type == "string":
            return self._tokenize_string()
        elif variable_type == "empty":
            return None  # Или какое значение соответствует empty
        elif variable_type == "boolean":
            return self._tokenize_boolean()
        else:
            raise ValueError(f"Unsupported variable type: {variable_type}")

    def _tokenize_integer(self) -> int:
        num_str = ""
        while self.char and self.char.isdigit():
            num_str += self.char
            self.advance()
        if not num_str:
            raise SyntaxError("Expected integer value")
        return int(num_str)

    def _tokenize_float(self) -> float:
        float_str = ""
        has_dot = False
        while self.char and (self.char.isdigit() or self.char == "."):
            if self.char == ".":
                if has_dot:
                    raise SyntaxError("Invalid float number")
                has_dot = True
            float_str += self.char
            self.advance()
        if not float_str:
            raise SyntaxError("Expected float value")
        return float(float_str)

    def _tokenize_string(self) -> str:
        if self.char != '"':
            raise SyntaxError("Expected string value to start with double quote")
        self.advance()
        string_value = ""
        while self.char and self.char != '"':
            string_value += self.char
            self.advance()
        if self.char != '"':
            raise SyntaxError("Expected string value to end with double quote")
        self.advance()
        return string_value

    def _tokenize_boolean(self) -> bool:
        if self.code[self.pos:self.pos + 4] == "true":
            self.pos += 4
            self.advance()
            return True
        elif self.code[self.pos:self.pos + 5] == "false":
            self.pos += 5
            self.advance()
            return False
        else:
            raise SyntaxError("Expected boolean value ('true' or 'false')")


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

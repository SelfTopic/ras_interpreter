from typing import Union, List
from ..ras_types import *
from ._tokenizer import _Tokenizer

class ValueTokenize(_Tokenizer):
    def __init__(self, code: str, types: List[str]):
        super().__init__(code)
        self.types = types

    def tokenize(self):
        self.skip_whitespace()
        if not self.char:
            return None

        value = self._tokenize_value()
        self.skip_whitespace()

        return (value, self.pos)

    def advance(self) -> None:
         self.pos += 1
         if self.pos < len(self.code):
             self.char = self.code[self.pos]
         else:
             self.char = ''

    def skip_whitespace(self):
        while self.char and self.char.isspace():
            self.advance()

    def _tokenize_value(self) -> Union[str, int, float, bool, None]:
        """Токенизирует значение переменной в зависимости от типа."""
        # ЧЕСТОР ТУТ ПЕРЕДЕЛАЙ А ТО ЗАЛУПА ВЫХОДИТ
        start_pos = self.pos
        for variable_type in self.types:
            if not variable_type in ALL_TYPES:
                raise ValueError(f"Unsupported variable type: {variable_type}")

            try:
                self.pos = start_pos
                self.char = self.code[self.pos]
                
                if variable_type == "integer":
                    return self._tokenize_integer()
                elif variable_type == "float":
                    return self._tokenize_float()
                elif variable_type == "string":
                    return self._tokenize_string()
                elif variable_type == "empty":
                    return EmptyType()
                elif variable_type == "bool":
                    return self._tokenize_bool()
            except:
                pass
        
        raise ValueError(f"Expected {', '.join(self.types[:-1]) if len(self.types) > 1 else self.types[0]}{f' or {self.types[-1]}' if len(self.types) > 1 else ''} value")

    def _tokenize_integer(self) -> int:
        num_str = ""
        
        while self.char and self.char.isdigit():
            num_str += self.char
            self.advance()
        
        if not num_str:
            raise SyntaxError("Expected integer value")
        return IntegerType(int(num_str))

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
        return FloatType(float(float_str))

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
        return StringType(string_value)

    def _tokenize_bool(self) -> bool:
        if self.code[self.pos:self.pos + 1] == "1!":
            self.pos += 1
            self.advance()
            return BoolType(True)
        elif self.code[self.pos:self.pos + 1] == "0!":
            self.pos += 1
            self.advance()
            return BoolType(False)
        else:
            raise SyntaxError("Expected boolean value (1! or 0!)")
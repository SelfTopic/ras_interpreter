from dataclasses import dataclass, field
from typing import List, Union, Tuple

from .type_tokens import (
    Function,
    Variable    
)
from .tokenize_variable import VariableTokenize  
from .tokenize_function import FunctionTokenize


@dataclass
class ClassDefinition:
    name: str
    variables: List[Variable] = field(default_factory=list)
    functions: List[Function] = field(default_factory=list)

class ClassTokenize:
    def __init__(self, code: str):
        self.code = code
        self.example = code
        self.pos = 0
        self.char = self.code[self.pos] if code else ''

    def tokenize(self):
        self.skip_whitespace()
        print(self.char)

        if not self.example.startswith("cl"):
            raise SyntaxError("Expected 'cl' keyword")
        self.pos += len("cl")
        self.advance()
        self.skip_whitespace()

        name = self._tokenize_name()
        self.skip_whitespace()

        if self.code[self.pos:self.pos + 2] != "::":
            raise SyntaxError("Expected '::' after class name")
        self.pos += 2
        self.advance()

        variables, functions = self._tokenize_body()
        self.skip_whitespace()

        if self.code[self.pos:self.pos + 2] != "::":
            print(self.char)
            raise SyntaxError("Expected '::' after class body")
        self.pos += 2
        self.advance()

        return ClassDefinition(name=name, variables=variables, functions=functions), self.pos

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
            raise SyntaxError("Expected class name")
        return name

    def _tokenize_body(self) -> tuple[List[Variable], List[Function]]:
        variables: List[Variable] = []
        functions: List[Function] = []

        while self.char:
            print(self.char)
            self.skip_whitespace()
            if self.code[self.pos:self.pos + 2] == "::":
                break  

            if self.code[self.pos:].startswith("local") or self.code[self.pos:].startswith("global"):
                variable, offset = VariableTokenize(self.code[self.pos:]).tokenize() 
                variables.append(variable)

                self.pos += offset
                self.advance()


            elif self.code[self.pos:].startswith("fn"):
                function, offset = FunctionTokenize(self.code[self.pos:]).tokenize()  
                functions.append(function)

                self.pos += offset 
                self.advance()
            elif self.code[self.pos:].startswith("#"): 
                while self.char and self.char != '\n':
                    self.advance()
                if self.char == '\n':
                    self.advance()
                continue 

            else:
                raise SyntaxError(f"Unexpected token {self.char} in class body")

        return variables, functions


if __name__ == '__main__':
    code_example = """cl MyClass :: local var :integer: << 10 # ::"""
    tokenizer = ClassTokenize(code_example)
    class_definition = tokenizer.tokenize()
    print(class_definition)

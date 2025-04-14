from dataclasses import dataclass, field
from typing import List, Union, Tuple, Optional

from .type_tokens import (
    Function,
    Variable    
)
from ._tokenizer import _Tokenizer
from .tokenize_variable import VariableTokenize
from .tokenize_value import ValueTokenize
from .tokenize_function import FunctionTokenize

from ..ras_types import EmptyType


@dataclass
class Class:
    name: str
    parent: Optional["Class"] = None
    variables: List[Variable] = field(default_factory=list)
    functions: List[Function] = field(default_factory=list)
    initialize: Function = None# field(default_factory=lambda: Function("default_init"))
    getters: dict[Variable, Function] = field(default_factory=dict)
    setters: dict[Variable, Function] = field(default_factory=dict)


class ClassTokenize(_Tokenizer):
    def __init__(self, code: str):
        super().__init__(code)
        # self.example = code

    def tokenize(self):
        self.skip_whitespace()
        print(self.char)

        # if not self.example.startswith("cl"):
        #     raise SyntaxError("Expected 'cl' keyword")
        self.pos += len("cl")
        self.advance()
        self.skip_whitespace()

        name = self._tokenize_name()
        self.skip_whitespace()

        if self.char == ":" and self.code[self.pos:self.pos + 2] != "::":
            parent = self._tokenize_parent()
            self.skip_whitespace()
            print("parent:", parent)
        else:
            parent = None

        if self.code[self.pos:self.pos + 2] != "::":
            raise SyntaxError("Expected '::' after class declaration")
        self.pos += 2
        self.advance()

        variables, functions, initialize, getters, setters = self._tokenize_body()
        self.skip_whitespace()
        print("self:code: ", self.code[self.pos:])

        if self.code[self.pos:self.pos + 2] != "::":
            print(self.char)
            raise SyntaxError("Expected '::' after class body")
        self.pos += 2
        self.advance()

        return Class(
            name=name,
            parent=parent,
            variables=variables,
            functions=functions,
            initialize=initialize,
            getters=getters,
            setters=setters
            ), self.pos

    def _tokenize_name(self) -> str:
        name = ""
        while self.char and (self.char.isalnum() or self.char == "_"):
            name += self.char
            self.advance()
        if not name:
            raise SyntaxError("Expected class name")
        return name

    def _tokenize_parent(self) -> str:
        parent = ""
        self.advance()
        self.skip_whitespace()
        
        while self.char != ":":
            print("Tokenize class parent, char: ", self.char)
            # self.pos += 1
            parent += self.char 
            self.advance()

        self.advance()
        
        return parent

    def _tokenize_body(self) -> tuple[List[Variable], List[Function]]:
        passed = 0
        to_pass = (
                    self.code[self.pos:].count("fn") + \
                    self.code[self.pos:].count("cl") + \
                    self.code[self.pos:].count("initialize") + \
                    self.code[self.pos:].count("get") + \
                    self.code[self.pos:].count("set") + \
                    self.code[self.pos:].count("con") + \
                    self.code[self.pos:].count("elcon") + \
                    self.code[self.pos:].count("noc") + \
                    self.code[self.pos:].count("whi") + \
                    self.code[self.pos:].count("for")
                ) * 2
        variables: List[Variable] = []
        functions: List[Function] = []
        initialize = None
        getters:   List[Function] = []
        setters:   List[Function] = []
        print("TO:PASS: ", to_pass)

        while passed <= to_pass:
            if self.code[self.pos : self.pos + 2] == "::":
                passed += 1
                self.pos += 1
            
            self.advance()
            print(self.char)
            self.skip_whitespace()
            if self.code[self.pos:self.pos + 2] == "::":
                break

            if self.code[self.pos:].startswith("#"): 
                while self.char and self.char != '\n':
                    self.advance()
                if self.char == '\n':
                    self.advance()
                continue

            elif not (self.code[self.pos:].startswith("initialize")
                    or self.code[self.pos:].startswith("get")
                    or self.code[self.pos:].startswith("set")
                    or self.code[self.pos:].startswith("fn")):
                # self.advance() #пропускаем пробел
                print(self.char)

                variable = VariableTokenize(self.code[self.pos:])
                name = variable._tokenize_name()
                variable.skip_whitespace()
                print(f"code: '{variable.code}'")

                if variable.char != ":":
                    raise SyntaxError("Expected ':' after variable name")
                variable.advance()

                data_types = variable._tokenize_type()
                variable.skip_whitespace()

                if variable.char != ":":
                    raise SyntaxError("Expected ':' after variable type")
                variable.advance()
                variable.skip_whitespace()
                print(f"abbunga: '{variable.code[variable.pos:variable.pos + 2]}'")
                if variable.code[variable.pos:variable.pos + 2] == "<<":

                    # raise SyntaxError("Expected '<<' after ':'")
                    variable.pos += 2
                    variable.advance()
                    variable.skip_whitespace()

                    value, offset = ValueTokenize(variable.code[variable.pos:], data_types).tokenize()
                    variable.pos += offset
                    variable.char = variable.code[variable.pos]
                else:
                    value = EmptyType()
                    # print(variable.pos, variable.)
                    variable.skip_whitespace()

                if variable.char != "#":
                    raise SyntaxError("Expected '#' at the end of variable declaration")
                #variable.pos += 1 # consume the hash
                #variable.advance()
                self.pos += variable.pos
                variables.append(Variable(name=name, value=value, data_types=data_types, is_local=False, is_global=False))

                self.advance()


            elif (self.code[self.pos:].startswith("initialize")
                  or self.code[self.pos:].startswith("fn")
                  or self.code[self.pos:].startswith("get")
                  or self.code[self.pos:].startswith("set")):
                function, offset = FunctionTokenize(self.code[self.pos:]).tokenize()  
                print("FUNCTION: ", function)
                if self.code[self.pos:].startswith("initialize"):
                    initialize = function
                elif self.code[self.pos:].startswith("get"):
                    getters.append(function)
                elif self.code[self.pos:].startswith("set"):
                    setters.append(function)
                else:
                    functions.append(function)

                self.pos += offset
                self.advance()

            else:
                raise SyntaxError(f"Unexpected token {self.char} in class body")

        return variables, functions, initialize, getters, setters


if __name__ == '__main__':
    code_example = """cl MyClass :: local var :integer: << 10 # ::"""
    tokenizer = ClassTokenize(code_example)
    class_definition = tokenizer.tokenize()
    print(class_definition)

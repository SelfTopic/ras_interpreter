from typing import Union, Tuple, List

from .tokenize_variable import Variable, VariableTokenize
from .tokenize_function import FunctionTokenize, Function
from .tokenize_class import ClassDefinition, ClassTokenize
from .tokenize_for import ForLoop, ForLoopTokenize
from .tokenize_while import WhileLoop, WhileLoopTokenize
from .tokenize_import import ImportStatement, ImportTokenize


class Tokenizer:
    def __init__(self, code: str):
        self.code = code
        self.pos = 0
        self.char = self.code[self.pos] if code else ''

    def advance(self) -> None:
        self.pos += 1
        if self.pos < len(self.code):
            self.char = self.code[self.pos]
        else:
            self.char = ''

    def skip_whitespace(self):
        while self.char and self.char.isspace():
            self.advance()

    def tokenize(self) -> List[Union[Variable, Function, ClassDefinition, ForLoop, WhileLoop, ImportStatement]]:
        tokens = []

        while self.char:
            print("tokenize; char", self.char)
            self.skip_whitespace()

            if self.code[self.pos:].startswith("local") or self.code[self.pos:].startswith("global"):
                variable, offset = VariableTokenize(self.code[self.pos:]).tokenize()
                tokens.append(variable)
                self.pos += offset
                self.advance()
            elif self.code[self.pos:].startswith("fn"):
                function, offset = FunctionTokenize(self.code[self.pos:]).tokenize()
                tokens.append(function)
                self.pos += offset
                self.advance()
            # elif self.code[self.pos:].startswith("cl"):
            #     class_def, offset = ClassTokenize(self.code[self.pos:]).tokenize()
            #     tokens.append(class_def)
            #     self.pos += offset
            #     self.advance()
            elif self.code[self.pos:].startswith("for"):
                for_loop, offset = ForLoopTokenize(self.code[self.pos:]).tokenize()
                tokens.append(for_loop)
                self.pos += offset
                self.advance()
            elif self.code[self.pos:].startswith("whi"):
                while_loop, offset = WhileLoopTokenize(self.code[self.pos:]).tokenize()
                tokens.append(while_loop)
                self.pos += offset
                self.advance()
            elif self.code[self.pos:].startswith("im"):
                import_statement, offset = ImportTokenize(self.code[self.pos:]).tokenize()
                tokens.append(import_statement)
                self.pos += offset
                self.advance()
            elif self.code[self.pos:].startswith("cl "):
                class_defintion, offset = ClassTokenize(self.code[self.pos:]).tokenize()
                tokens.append(class_defintion)
                self.pos += offset 
                self.advance()
            elif self.code.startswith("#"):  
                while self.char and self.char != '\n':
                    self.advance()
                if self.char == '\n':
                    self.advance()
            else:
                raise SyntaxError(f"Unexpected token {self.char} at position {self.pos}")

        return tokens


if __name__ == '__main__':
    code_example = """
local my_var :integer: << 10 #

fn my_func < param :integer: ++ param2 :string: :: 
    local copy :string: << param2 * param #
    print: copy # 
::

for i << my_list :: 
    print: i # 
::

whi :true: :: 
    print: "looping" # 
::

im my_module--alias
    """

    tokenizer = Tokenizer(code_example)
    tokens = tokenizer.tokenize()

    print(tokens)

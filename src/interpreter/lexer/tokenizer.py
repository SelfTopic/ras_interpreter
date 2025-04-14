from typing import Union, Tuple, List

from ._tokenizer import _Tokenizer
from .tokenize_variable import Variable, VariableTokenize
from .tokenize_function import FunctionTokenize, Function
from .tokenize_class import Class, ClassTokenize
from .tokenize_for import ForLoop, ForLoopTokenize
from .tokenize_while import WhileLoop, WhileLoopTokenize
from .tokenize_import import ImportStatement, ImportTokenize


class Tokenizer(_Tokenizer):
    def __init__(self, code: str):
        super().__init__(code)
        # self.code = code
        # self.pos = 0
        # self.char = self.code[self.pos] if code else ''

    def tokenize(self) -> List[Union[Variable, Function, Class, ForLoop, WhileLoop, ImportStatement]]:
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
            elif self.code[self.pos:].startswith("cl"):
                class_defintion, offset = ClassTokenize(self.code[self.pos:]).tokenize()
                tokens.append(class_defintion)
                self.pos += offset
                self.advance()
                print(f"MYCODE: '{self.code[self.pos:]}'")
            elif self.code.startswith("#"):  
                while self.char and self.char != '\n':
                    self.advance()
                if self.char == '\n':
                    self.advance()
            else:
                if self.char:
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

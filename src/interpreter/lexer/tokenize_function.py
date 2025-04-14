# _tokenize_params() и _tokenize_param() чекни

from .type_tokens import Function, Param, ParamDefaultValue, NoParamDefaultValue
from ._tokenizer import _Tokenizer
from .tokenize_value import ValueTokenize

class FunctionTokenize(_Tokenizer):
    def __init__(self, code: str):
        super().__init__(code)

    def tokenize(self):
        print(f"THIS CODE: '''{self.code}'''")
        function_name = self._tokenize_name()
        print(f"tokenize name", function_name)
        if function_name != "initialize":
            return_types = self._tokenize_return_types()
        else:
            return_types = "self"
        print(f"tokenize return types", return_types)
        params = self._tokenize_params()
        self.skip_whitespace()
        if not self.code[self.pos : self.pos + 2] == "::":
            raise SyntaxError("Expected '::' after params")
        self.pos += 2
        self.char = self.code[self.pos]
        body = self._tokenize_body()

        return Function(
            name=function_name,
            params=params,
            body=body,
            return_types=[return_type.strip() for return_type in return_types.split("++")]
        ), self.pos

    def advance(self) -> None:
        self.pos += 1
        if self.pos < len(self.code):
            self.char = self.code[self.pos]
        else:
            self.char = ''  


    def _tokenize_body(self) -> str:
        body = ""
        passed = 0
        to_pass = (
                    self.code[self.pos:].count("fn") + \
                    self.code[self.pos:].count("cl") + \
                    self.code[self.pos:].count("con") + \
                    self.code[self.pos:].count("elcon") + \
                    self.code[self.pos:].count("noc") + \
                    self.code[self.pos:].count("whi") + \
                    self.code[self.pos:].count("for")
                ) * 2

        while passed <= to_pass:
            if self.code[self.pos : self.pos + 2] == "::":
                passed += 1
                if passed <= to_pass:
                    body += "::"
                self.pos += 1
            else:
                body += self.char
            self.advance()

        return body


    def _tokenize_name(self) -> str:

        function_name = ""

        if self.code.startswith("fn"):
            self.pos = 2
            self.advance()
        elif self.code.startswith("get") or self.code.startswith("set"):
            self.pos = 3
            self.advance()
        # elif self.code.startswith("initialize"):
        #     self.pos = 10
        #     self.advance()

        while self.char != " ":

            if not self.char: 
                break 

            if self.char.isspace():
                self.advance()
                continue

            function_name += self.char
            self.advance()

        self.advance() 
        return function_name.strip()
    
    def skip_whitespace(self):
        while self.char and self.char.isspace():
            self.advance()
    
    def _tokenize_return_types(self) -> str:

        types_value = ""

        self.skip_whitespace()

        if self.char != ":":
            raise Exception(f"Ожидалось: operator :type:, получено: {self.char}")
        self.advance()
        
        while self.char != ":":
            print("Tokenize return type, char: ", self.char)
            # self.pos += 1
            types_value += self.char 
            self.advance()

        self.advance()
        
        return types_value


    def _tokenize_param(self, code: str) -> Param:

        name_param = ""
        data_types = ""
        colon_count = 0

        param_tokenizer = FunctionTokenize(code)
        param_tokenizer.pos = 0
        param_tokenizer.char = param_tokenizer.code[param_tokenizer.pos] if param_tokenizer.code else ''

        while param_tokenizer.char != '':
            # print("122: ", param_tokenizer.char)
            if param_tokenizer.char == ':':
                colon_count += 1
                param_tokenizer.advance()
                if colon_count == 1:
                    continue
                else:
                    break

            if colon_count == 0:
                 name_param += param_tokenizer.char
            elif colon_count == 1:
                data_types += param_tokenizer.char

            param_tokenizer.advance()

        if colon_count != 2:
            raise Exception(f"Ошибка токенизации параметра: Ожидается 'name:type:', получено {code}")
        
        types = [data_type.strip() for data_type in data_types.split("++")]
        
        param_tokenizer.advance()
        param_tokenizer.skip_whitespace()
        
        if code[param_tokenizer.pos:param_tokenizer.pos + 2] == "<<":
            value, offset = ValueTokenize(code[param_tokenizer.pos+2:], types).tokenize()
            value = ParamDefaultValue(value)
        else:
            value = NoParamDefaultValue()

        param = Param(
            name=name_param.strip(),
            types=types,
            value=value
        )

        return param


    def _tokenize_params(self) -> list[Param]:

        tokenized_param = ""
        params: list[Param] = []
        param_string = ""

        self.skip_whitespace()
        if not self.char == "<":
            Exception(f"Ошибка токенизации параметра: Ожидается '<', получено {self.char}")
        self.advance()
        start_params_index = self.pos
        
        # print("157:  ", self.pos, f"'{self.char}'")

        while self.char != '':
            if self.code[self.pos : self.pos + 2] == "::":
                break

            param_string += self.char
            self.advance()

        if not param_string:
            return params

        param_string = param_string.strip() 
        params_list = param_string.split("++")

        for param_code in params_list:
            print("pc:", param_code)
            if param_code.strip():
                params.append(self._tokenize_param(param_code))

        return params


if __name__ == '__main__':
    source_code = f"""fn nameFunc < param:integer: ++ param2:string: ::
print: param #
::"""

    lexer = FunctionTokenize(code=source_code)
    tokens = lexer.tokenize()

    print(tokens)

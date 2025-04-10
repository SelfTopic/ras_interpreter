from .type_tokens import Function, Param

class FunctionTokenize:

    def __init__(
        self,
        code: str
    ):
        self.code = code
        self.pos = 0
        self.char = self.code[self.pos] if code else '' 

    def tokenize(self):

        function_name = self._tokenize_name()
        print(f"tokenize name", function_name)
        return_type = self._tokenize_return_type()
        print(f"tokenize return type", return_type)
        params = self._tokenize_params()
        body = self._tokenize_body()

        return Function(
            name=function_name,
            params=params,
            body=body,
            return_type=return_type
        ), self.pos

    def advance(self) -> None:
        self.pos += 1
        if self.pos < len(self.code):
            self.char = self.code[self.pos]
        else:
            self.char = ''  


    def _tokenize_body(self) -> str:

        count_operators = 0
        body = ""

        while self.char != '': 

            if self.char == ":":
                self.advance()

                if self.char == ":":
                    count_operators += 1

                    if count_operators == 2:
                        self.advance() 
                        return body

                    self.advance()
                    continue

            body += self.char
            self.advance()

        return body


    def _tokenize_name(self) -> str:

        function_name = ""

        if self.code.startswith("fn"):
            self.pos = 2 
            self.advance() 

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
    
    def _tokenize_return_type(self) -> str:

        type_value = ""

        self.skip_whitespace()

        if self.char != ":":
            raise Exception(f"Ожидалось: operator :type:, получено: {self.char}")
        self.advance()
        
        while self.char != ":":
            print("Tokenize return type, char: ", self.char)
            self.pos += 1
            self.advance()
            type_value += self.char 

        self.advance()
        
        return type_value


    def _tokenize_param(self, code: str) -> Param:

        name_param = ""
        data_type = ""
        colon_count = 0

        param_tokenizer = FunctionTokenize(code)
        param_tokenizer.pos = 0
        param_tokenizer.char = param_tokenizer.code[param_tokenizer.pos] if param_tokenizer.code else ''

        while param_tokenizer.char != '':
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
                data_type += param_tokenizer.char

            param_tokenizer.advance()

        if colon_count != 2:
            raise Exception(f"Ошибка токенизации параметра: Ожидается 'name:type:', получено {code}")


        param = Param(
            name=name_param.strip(),
            type=data_type.strip()
        )

        return param


    def _tokenize_params(self) -> list[Param]:

        tokenized_param = ""
        params: list[Param] = []
        param_string = ""

        start_params_index = self.pos

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

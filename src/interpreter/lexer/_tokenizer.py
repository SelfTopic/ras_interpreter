class _Tokenizer:
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
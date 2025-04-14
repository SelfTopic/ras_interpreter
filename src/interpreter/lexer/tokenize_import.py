from dataclasses import dataclass
from typing import List
from ._tokenizer import _Tokenizer

@dataclass
class ImportStatement:
    filenames: List[str]

class ImportTokenize(_Tokenizer):
    def __init__(self, code: str):
        super().__init__(code)

    def tokenize(self) -> ImportStatement:
        """Токенизирует оператор импорта."""
        self.skip_whitespace()

        if not self.code.startswith("im"):
            raise SyntaxError("Expected 'im' keyword")
        self.pos += len("im")
        self.advance()
        self.skip_whitespace()

        filenames = self._tokenize_filenames()
        return ImportStatement(filenames=filenames), self.pos

    def advance(self) -> None:
        self.pos += 1
        if self.pos < len(self.code):
            self.char = self.code[self.pos]
        else:
            self.char = ''

    def skip_whitespace(self):
        while self.char and self.char.isspace():
            self.advance()

    def _tokenize_filenames(self) -> List[str]:
        """Токенизирует список имен файлов."""
        filenames = []
        filename = ""
        while self.char:
            if self.char == ",":
                filenames.append(filename.strip())
                filename = ""
                self.advance()
                self.skip_whitespace()
            elif self.char == '-':
                 self.advance()
                 while self.char and (self.char.isalnum() or self.char == "_"):
                    filename += self.char
                    self.advance()

                 filenames.append(filename.strip())
                 filename = ""
                 if self.char == ',':
                    self.advance()
                    self.skip_whitespace()
            else:
                filename += self.char
                self.advance()
        if filename:
            filenames.append(filename.strip())
        return filenames

if __name__ == '__main__':
    code_example = "im filename--name, filename2--name2"
    tokenizer = ImportTokenize(code_example)
    import_statement = tokenizer.tokenize()
    print(import_statement)

    code_example2 = "im file1--var1, file2--var2, file3--var3"
    tokenizer2 = ImportTokenize(code_example2)
    import_statement2 = tokenizer2.tokenize()
    print(import_statement2)
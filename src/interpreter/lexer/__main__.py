from .tokenizer import Tokenizer 

code = f"""

fn main :integer: < ::
  >> 10 # 
::
"""

tokenizer = Tokenizer(code) 

tokens = tokenizer.tokenize()
print(tokens)
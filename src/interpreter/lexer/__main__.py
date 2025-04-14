from .tokenizer import Tokenizer

code = f"""
fn main :integer ++ string: <  bebra :integer: << 12345 ++ adolf :string: ::
  fn myFunction :empty: < bidon :integer: :: ::
  for number << array :: >> "adolf" ::
  whi :true: ::::
  >> 10 #
::
"""

code = """
local a :
  string ++
  integer
: << 123 #
"""

code = f"""
cl Child :Parent: ::
  # myVariable :integer: << 12345 #
  # anotherVariable :string: << "Adolf Hitler" #

  # fn main : integer ++ string : < param1 :string: << "bebra" ::
  #   >> "a" #
  # ::

  initialize < name :string: ++ age :integer: ::
    name << name #
    age << age #
  ::
::
"""

code = """
cl Animal ::
  name :string: #
  age :integer: #

  initialize < name:string: ++ age:integer: ::
    name << name #
    age << age #
  ::

  get name :string: < ::
    >> name #
  ::

  set name :empty: < newName:string: ::
    name << newName #
  ::

  get age :integer: < ::
    >> age #
  ::

  set age :empty: < newAge:integer: ::
    age << newAge #
  ::

  fn printInfo :empty: < ::
    print: "Name: "#
    print: name #
    print: ", Age: "#
    print: age #
    print: "#" #
  ::
::

cl Dog :Animal: ::
  breed :string: #

  initialize < name:string: ++ age:integer: ++ breed:string: ::
    root--initialize: name, age #
    breed << breed #
  ::

  get breed :string: < ::
    >> breed #
  ::

  set breed :empty: < newBreed:string: ::
    breed << newBreed #
  ::

  fn bark :empty: < ::
    print: "Woof!#" #
  ::

  fn printInfo :empty: < ::
    root--printInfo: #
    print: ", Breed: "#
    print: breed #
    print: "#" #
  ::
::
"""

code = """
fn fun1 :string: < param1 :integer: ++ param2 :string++integer: ::
  print: "adolf" #
  >> "hitler" #
::

fn fun2 :empty: < ::
  print: 1 #
::
"""

tokenizer = Tokenizer(code) 

tokens = tokenizer.tokenize()
print(tokens)
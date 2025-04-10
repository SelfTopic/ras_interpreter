from dataclasses import dataclass 
from .params import Param

@dataclass 
class Function:
    name: str 
    params: list[Param]
    return_type: str
    body: str 

    
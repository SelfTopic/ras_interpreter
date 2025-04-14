from dataclasses import dataclass 
from ...ras_types import StringType
from typing import Union, List

@dataclass 
class Param:
    name: StringType
    types: List[StringType]
    value: Union[str, int, float, bool, None]

class ParamDefaultValue:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"ParamDefaultValue({self.value})"

class NoParamDefaultValue:
    def __repr__(self):
        return f"NoParamDefaultValue()"
# variable.py

from typing import Union, Optional
from ...ras_types import (
    StringType, 
    IntegerType,
    BoolType,
    EmptyType,
    FloatType,
    ListType,
    TupleType,
    DictType
)

DATA_TYPE = Union[
    StringType,
    IntegerType,
    BoolType,
    EmptyType,
    FloatType,
    ListType,
    TupleType,
    DictType
]

class Variable:
    def __init__(self,
                 name: StringType,
                 data_types: type[DATA_TYPE],
                 value: Optional[DATA_TYPE] = None,
                 is_local: bool = False,
                 is_global: bool = False,
                 path: Optional[StringType] = None,
                 scope_id: Optional[int] = None):  # Идентификатор области видимости

        self.is_local = is_local
        self.is_global = is_global
        self.data_types = data_types
        self.name = name
        self.path = path
        self.value = value
        self.scope_id = scope_id

    def __repr__(self):
        return f"Variable(name={self.name}, types={self.data_types}, value={self.value}, is_local={self.is_local}, is_global={self.is_global}, path={self.path}, scope_id={self.scope_id})"
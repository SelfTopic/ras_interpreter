from typing import Union
from .ras_types import (
    string
)

from .base import DATA_TYPE

class Variable:
    is_local: bool 
    is_global: bool 

    data_type: DATA_TYPE
    name: string
    path: string 
    value: DATA_TYPE

from .ras_types import (
    string,
    integer,
    empty    
)

from typing import Union

DATA_TYPE = Union[
    string,
    integer,
    empty,
    float,
    list,
    tuple,
    dict
]
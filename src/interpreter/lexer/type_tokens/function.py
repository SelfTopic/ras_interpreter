from dataclasses import dataclass
from .params import Param

@dataclass
class Function:
    name: str
    params: list[Param]
    return_types: list[str]
    body: str


@dataclass
class Getter:
    root: None
    name: str
    params: list[Param]
    return_types: list[str]
    body: str


@dataclass
class Setter:
    root: None
    name: str
    params: list[Param]
    return_types: list[str]
    body: str
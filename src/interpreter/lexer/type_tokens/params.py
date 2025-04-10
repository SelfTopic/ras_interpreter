from dataclasses import dataclass 
from ...ras_types import StringType

@dataclass 
class Param:
    name: StringType
    type: StringType
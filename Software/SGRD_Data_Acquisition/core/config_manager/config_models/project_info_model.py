from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class ProjectInfo:
    ID: str
    Name : str
    Description: str
    Version: str
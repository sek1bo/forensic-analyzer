from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class FileData:
    name: str
    path: str
    size: int
    category: str
    metadata: Dict[str, str]
    suspicious: bool
    analysis: Dict[str, Any]

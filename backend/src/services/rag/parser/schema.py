# backend/src/services/rag/parser/schema.py

from dataclasses import dataclass, asdict
from typing import List, Optional

@dataclass
class POI:
    category: str
    name: str
    description: str
    menu: Optional[str]
    location: Optional[str]
    phone: Optional[str]
    tags: List[str]

    def to_dict(self):
        return asdict(self)
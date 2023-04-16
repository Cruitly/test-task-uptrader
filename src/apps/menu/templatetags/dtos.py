from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class MenuDTO:
    id: int
    title: str
    slug: str
    parent_id: Optional[int]
    children: List['MenuDTO'] = field(default_factory=list)

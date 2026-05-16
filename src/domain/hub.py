from enum import Enum
from dataclasses import dataclass, field
from . import Connection


class HubType(Enum):
    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"


@dataclass
class Hub:
    name: str
    position: tuple[int, int]
    max_drones: int = 1
    hub_type: HubType = HubType.NORMAL
    color: str = "default"
    connections: list[Connection] = field(default_factory=list)

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .connection import Connection


class ZoneType(Enum):
    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"


class HubRole(Enum):
    HUB = "hub"
    START = "start_hub"
    END = "end_hub"


@dataclass
class Hub:
    name: str
    position: tuple[int, int]
    role: HubRole
    zone: ZoneType = ZoneType.NORMAL
    max_drones: int = 1
    color: str = "default"
    connections: list[Connection] = field(default_factory=list)

    @property
    def is_start(self) -> bool:
        return self.role is HubRole.START

    @property
    def is_end(self) -> bool:
        return self.role is HubRole.END

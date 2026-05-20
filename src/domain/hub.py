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
    color: str | None = None
    connections: list[Connection] = field(default_factory=list)

    # @property
    # def is_start(self) -> bool:
    #     return self.role is HubRole.START

    # @property
    # def is_end(self) -> bool:
    #     return self.role is HubRole.END

    def movement_cost(self) -> int:
        if self.zone is ZoneType.RESTRICTED:
            return 2
        return 1

    def is_traversable(self) -> bool:
        return self.role is not ZoneType.BLOCKED

    def is_priority(self) -> bool:
        return self.role is ZoneType.PRIORITY

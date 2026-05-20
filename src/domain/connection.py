from __future__ import annotations

from typing import TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    from .hub import Hub


@dataclass
class Connection:
    hubs: tuple[Hub, Hub]
    max_link_capacity: int = 1
    occupation: int = 0

    def get_neighbor(self, hub) -> Hub:
        if self.hubs[0] == hub:
            return self.hubs[1]
        elif self.hubs[1] == hub:
            return self.hubs[0]
        else:
            raise ValueError("hub not in connection")

    def is_available(self) -> bool:
        return self.occupation != self.max_link_capacity

    def remaining_capacity(self) -> int:
        return self.max_link_capacity - self.occupation

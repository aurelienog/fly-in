from __future__ import annotations
import math

from typing import TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    from .hub import Hub


@dataclass
class Connection:
    hubs: tuple[Hub, Hub]
    max_link_capacity: int = 1
    occupation: int = 0
    base_cost = None

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

    def get_distance(self, target: Hub) -> float:
        # distance = √((x2-x1)² + (y2-y1)²)
        source = self.get_neighbor(target)

        dx = source.x - target.x
        dy = source.y - target.y

        return math.sqrt(dx*dx + dy*dy)

    def get_cost(self, target: Hub):
        """
        Returns the intrinsic traversal cost of this edge.

        This cost is static and independent from the simulation state.

        Includes:
            - geometric distance
            - zone movement modifier
            - structural penalties

        Does NOT include:
            - congestion
            - reservations
            - occupancy
            - timestep-dependent costs
        """

        cost = self.get_distance(target)

        if target.zone == "restricted":
            cost += 5

        elif target.zone == "priority":
            cost -= 2

        return max(1, cost)

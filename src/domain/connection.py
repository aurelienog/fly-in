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
    base_cost: float | None = None

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

    def get_distance(self) -> float:
        # distance = √((x2-x1)² + (y2-y1)²)
        hub1, hub2 = self.hubs

        dx = hub1.position[0] - hub2.position[0]
        dy = hub1.position[1] - hub2.position[1]

        return math.sqrt(dx*dx + dy*dy)

    def get_cost(self, destination: Hub):
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

        cost = self.get_distance()

        if destination.zone == "blocked":
            return math.inf

        if destination.zone == "restricted":
            cost += 2

        elif destination.zone == "priority":
            cost -= 0.1

        return max(1, cost)

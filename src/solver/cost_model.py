from dataclasses import dataclass
from ..domain import Connection, Hub, ZoneType

import math


@dataclass
class CostModel:
    """Cost model used for route planning and pathfinding algorithms.

    This class centralizes all routing heuristics and cost calculations
    used by planning algorithms such as Dijkstra, A*, or space-time
    planners.

    The cost model ensures that routing logic remains independent from
    pathfinding algorithms by delegating all cost and heuristic
    computations to a single consistent interface.

    Attributes:
        (No stored attributes in this model; it acts as a stateless
        computation component.)
    """

    def edge_cost(
        self,
        connection: Connection,
        target: Hub,
    ):
        """Compute the traversal cost of using a connection.

        The cost represents the "weight" of moving through a connection
        toward a target hub. It may include static and dynamic factors
        such as distance, congestion, and zone penalties.

        Args:
            connection: The network connection being evaluated.
            target: The destination hub reached through the connection.

        Returns:
            A non-negative traversal cost. Lower values indicate more
            desirable routes. Returns ``math.inf`` if the target hub
            is not traversable.
        """
        cost = (
            connection.get_distance()
            + target.movement_cost()
        )

        if target.zone is ZoneType.BLOCKED:
            return math.inf

        utilization = (
            connection.occupation
            / connection.max_link_capacity
        )

        cost += utilization * 5.0

        if target.zone is ZoneType.PRIORITY:
            cost *= 0.9

        return cost

    def heuristic(
        self,
        current_hub: Hub,
        target_hub: Hub
    ) -> float:
        """Estimate the remaining cost from a hub to the target.

        This heuristic is used by informed search algorithms such as A*.
        It provides an optimistic estimate of the remaining traversal
        cost based on geometric distance.

        Args:
            current_hub: The current position in the search.
            target_hub: The goal hub.

        Returns:
            A heuristic cost estimate. Always non-negative.
        """

        dx = (current_hub.position[0] - target_hub.position[0])

        dy = (current_hub.position[1] - target_hub.position[1])

        return math.sqrt(dx*dx + dy*dy)

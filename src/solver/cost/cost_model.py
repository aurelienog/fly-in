from dataclasses import dataclass
from ...domain import Connection, Hub, ZoneType

import math


@dataclass
class CostModel:
    """
    Computes the traversal cost of a connection during route planning.

    This class centralizes all routing heuristics and penalties used by
    planning algorithms such as Dijkstra, Space-Time A*, or CBS.

    The returned value represents the "weight" of traversing a connection
    at a given simulation timestep.

    Lower values indicate more desirable routes.

    The cost can combine multiple factors, for example:

        - physical distance
        - monetary/energy cost
        - hub congestion
        - link occupancy
        - restricted zones penalties
        - priority zones rewards
        - dynamic simulation conditions

    Purpose
    -------
    Keep routing logic independent from planning algorithms.

    Algorithms should NOT implement their own cost formulas.
    Instead, they should delegate cost computation to CostModel.

    Example
    -------
    cost = model.edge_cost(
        connection=conn,
        timestep=12
    )

    Example formula
    ---------------
    total_cost =
        distance_weight * connection.distance
        + congestion_weight * connection.load
        + restricted_penalty

    Notes
    -----
    The cost function is intentionally configurable and may evolve
    during experimentation or benchmarking.
    """

    def edge_cost(
        self,
        connection: Connection,
        target: Hub,
    ):
        """
        Computes the traversal cost of using a connection at a specific
        simulation timestep.

        If timestep is provided, dynamic/time-dependent penalties
        may be applied.

        Parameters
        ----------
        connection : Connection
            The network edge being evaluated.

        timestep : int
            Current simulation time.

            Useful for time-dependent costs such as:
                - congestion
                - reservations
                - dynamic penalties
                - traffic scheduling

        Returns
        -------
        float

            Non-negative traversal weight.

            Lower values represent cheaper / preferred routes.

            Higher values represent expensive, congested,
            risky, or restricted routes.

        Notes
        -----
        The returned value is consumed directly by pathfinding algorithms.

        Typical components:

            base_distance
            + travel_cost
            + congestion_penalty
            + restriction_penalty
            - priority_bonus

        Example
        -------
        return (
            connection.get_distance()
            + 10 * connection.current_load
        )
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
        # cost: int | float = connection.get_cost(target)

        # if timestep is not None:

        #     # future logic
        #     # reservation_table lookup
        #     # congestion prediction
        #     # dynamic penalties

        #     pass

        # return cost

    def heuristic(
        self,
        current_hub: Hub,
        target_hub: Hub
    ) -> float:
        """
        Estimates the remaining cost from a node to the goal.

        Used by heuristic planners such as A*.

        Returns an optimistic approximation of the remaining route cost.

        Lower estimates improve optimality guarantees.
        """

        dx = (current_hub.position[0] - target_hub.position[0])

        dy = (current_hub.position[1] - target_hub.position[1])

        return math.sqrt(dx*dx + dy*dy)

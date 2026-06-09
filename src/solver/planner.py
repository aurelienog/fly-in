import heapq
from itertools import count

from .cost_model import CostModel
from .reservation_table import ReservationTable

from .models import (
    SpaceTimeState,
    EdgeTimeInterval,
)

from ..domain import (
    Hub,
)


class SpaceTimeAStarPlanner():
    """Space-time A* planner for multi-agent pathfinding.

    This planner computes collision-free paths in a time-expanded graph
    where nodes represent (hub, timestep) states. It integrates:

        - A* search over space-time states
        - Heuristic guidance via geometric distance
        - Node and edge reservation constraints
        - Waiting and movement actions

    The planner is designed for multi-agent systems where agents must
    avoid both spatial and temporal conflicts.
    """

    def __init__(self, reservation_table: ReservationTable) -> None:
        """Initialize the planner with a shared reservation table.

        Args:
            reservation_table: Global structure used to track occupied
                nodes and edges over time.
        """
        self.reservation_table = reservation_table

    def plan(
        self,
        start: Hub,
        goal: Hub,
    ) -> list[SpaceTimeState]:
        """Compute a collision-free space-time path from start to goal.

        The algorithm performs A* search over a time-expanded graph.
        It considers both movement and waiting actions, while enforcing
        constraints from the reservation table.

        Args:
            start: Starting hub.
            goal: Target hub.

        Returns:
            A list of space-time states representing the path from start
            to goal. Returns an empty list if no valid path is found.
        """

        cost_model = CostModel()
        counter = count()

        start_state = SpaceTimeState(
            hub=start,
            timestep=0
        )

        g_score: dict[SpaceTimeState, float] = {start_state: 0.0}

        came_from: dict[
            SpaceTimeState, SpaceTimeState | None
        ] = {start_state: None}

        queue: list[tuple[float, int, SpaceTimeState]] = []

        initial_f = cost_model.heuristic(start, goal)

        heapq.heappush(
            queue,
            (
                initial_f,
                next(counter),
                start_state
            )
        )

        while queue:

            priority, _, current = (
                heapq.heappop(queue)
            )

            expected_priority = (
                g_score[current]
                +
                cost_model.heuristic(
                    current.hub,
                    goal
                )
            )

            # stale queue entry

            if priority > expected_priority:
                continue

            if current.hub == goal:

                return self.reconstruct_path(
                    came_from,
                    current
                )

            # normal moves

            for connection in current.hub.connections:

                neighbor = (connection.get_neighbor(current.hub))

                if not neighbor.is_traversable():
                    continue

                next_time = current.timestep + neighbor.movement_cost()
                neighbor_state = SpaceTimeState(neighbor, next_time)
                #
                # NODE CHECK
                #
                if not self.reservation_table.state_available(neighbor_state):
                    continue
                #
                # EDGE CHECK (INTERVAL)
                #
                interval = EdgeTimeInterval(
                    connection=connection,
                    t_start=current.timestep,
                    t_end=next_time
                )
                if not self.reservation_table.interval_available(interval):
                    continue

                #
                # COST
                #
                edge_cost = cost_model.edge_cost(connection, neighbor)

                tentative_g = g_score[current] + edge_cost
                if (
                    neighbor_state not in g_score
                    or tentative_g < g_score[neighbor_state]
                ):
                    g_score[neighbor_state] = tentative_g
                    came_from[neighbor_state] = current

                    f_score = tentative_g + cost_model.heuristic(neighbor, goal)

                    heapq.heappush(
                        queue,
                        (f_score, next(counter), neighbor_state)
                    )

            # WAIT action

            wait_state = SpaceTimeState(current.hub, current.timestep + 1)

            if self.reservation_table.state_available(wait_state):

                tentative_g = g_score[current] + 1

                if (
                    wait_state not in g_score
                    or tentative_g < g_score[wait_state]
                ):

                    g_score[wait_state] = tentative_g
                    came_from[wait_state] = current

                    f_score = tentative_g + cost_model.heuristic(current.hub, goal)

                    heapq.heappush(
                        queue,
                        (f_score, next(counter), wait_state)
                    )

        return []

    def reconstruct_path(
        self,
        came_from: dict[
            SpaceTimeState,
            SpaceTimeState | None
        ],
        current: SpaceTimeState | None
    ) -> list[SpaceTimeState]:
        """Reconstruct the path from goal to start.

        Args:
            came_from: Mapping of each state to its predecessor.
            current: Final state reached by the search.

        Returns:
            Ordered list of states from start to goal.
        """

        path: list[
            SpaceTimeState
        ] = []

        while current is not None:

            path.append(current)

            current = came_from[current]

        path.reverse()

        return path

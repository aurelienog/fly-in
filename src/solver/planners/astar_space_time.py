import heapq

from .base_planner import BasePlanner
from ..cost.cost_model import CostModel
from ..simulation.reservation_table import ReservationTable
from ..models import CBSConstraint, SpaceTimeState
from ...domain import Connection, Hub, Network


class SpaceTimeAStarPlanner(BasePlanner):
    def __init__(
            self,
            reservation_table: ReservationTable | None = None,
            constraints: set[CBSConstraint] | None = None
            ):
        self.reservation_table = (
            reservation_table if reservation_table is not None else None
            )

        self.constraints = constraints if constraints is not None else set()

    def plan(self, start: Hub, goal: Hub, network: Network) -> list[SpaceTimeState]:

        cost_model = CostModel()

        start_state = SpaceTimeState(
            hub=start,
            timestep=0
        )

        g_score: dict[SpaceTimeState, float] = {
            start_state: 0
        }

        came_from: dict[SpaceTimeState, SpaceTimeState | None] = {
            start_state: None
        }

        queue: list[tuple[float, SpaceTimeState]] = []

        heapq.heappush(
            queue,
            (0, start_state)
        )

        while queue:

            priority, current = (
                heapq.heappop(queue)
            )

            expected_priority = (
                g_score[current] + cost_model.heuristic(current.hub, goal)
            )

            if priority > expected_priority:
                continue

            if current.hub == goal:

                return self.reconstruct_path(came_from, current)

            for connection in current.hub.connections:

                neighbor = connection.get_neighbor(current.hub)

                if not neighbor.is_traversable():
                    continue

                movement_turns = neighbor.movement_cost()

                next_time = (current.timestep + movement_turns)

                if self.is_forbidden(
                    neighbor,
                    connection,
                    next_time
                ):
                    continue

                if (
                    self.reservation_table is not None
                    and not self.reservation_table.hub_available(
                        neighbor,
                        next_time
                    )
                ):
                    continue

                if (
                    self.reservation_table is not None
                    and not self.reservation_table.connection_available(
                        connection,
                        next_time
                    )
                ):
                    continue

                neighbor_state = SpaceTimeState(
                    hub=neighbor,
                    timestep=next_time
                )

                edge_cost = cost_model.edge_cost(connection,
                                                 neighbor,
                                                 timestep=next_time)

                tentative_g = (g_score[current] + edge_cost)

                if (
                    neighbor_state not in g_score
                    or tentative_g < g_score[neighbor_state]
                ):

                    g_score[neighbor_state] = tentative_g

                    came_from[neighbor_state] = current

                    f_score = (tentative_g + cost_model.heuristic(neighbor, goal))

                    heapq.heappush(queue, (f_score, neighbor_state))

        return []

    def reconstruct_path(
        self,
        came_from: dict[SpaceTimeState, SpaceTimeState | None],
        current: SpaceTimeState | None
    ) -> list[SpaceTimeState]:

        path: list[SpaceTimeState] = []

        while current is not None:
            path.append(current)
            current = came_from[current]

        path.reverse()
        return path

    def is_forbidden(
        self,
        neighbor: Hub,
        connection: Connection,
        timestep: int
    ) -> bool:

        for constraint in self.constraints:

            # vertex constraint

            if (
                constraint.hub == neighbor
                and constraint.timestep == timestep
            ):
                return True

            # edge constraint

            if (
                constraint.connection == connection
                and constraint.timestep == timestep
            ):
                return True

        return False

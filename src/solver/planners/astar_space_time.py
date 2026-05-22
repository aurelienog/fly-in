import heapq

from .base_planner import BasePlanner
from ..cost.cost_model import CostModel
from ..simulation.reservation_table import ReservationTable
from ..models.space_time_state import SpaceTimeState

from ...domain import Hub, Network


class SpaceTimeAStarPlanner(BasePlanner):
    def __init__(
            self,
            reservation_table: ReservationTable
        ):
            self.reservation_table: ReservationTable = reservation_table

    def plan(
        self,
        start: Hub,
        goal: Hub,
        _network: Network,
    ) -> list[Hub]:

        cost_model: CostModel = CostModel()

        start_state: SpaceTimeState = SpaceTimeState(
            hub=start,
            timestep=0
        )

        g_score: dict[SpaceTimeState, float] = {
            start_state: 0
        }

        came_from: dict[
            SpaceTimeState,
            SpaceTimeState | None
        ] = {
            start_state: None
        }

        queue: list[tuple[int, SpaceTimeState]] = []

        heapq.heappush(queue, (0, start_state))

        while queue:

            priority, current = heapq.heappop(
                queue
            )

            if priority > (g_score[current] + cost_model.heuristic(current.hub, goal)):
                continue

            if current.hub == goal:

                return self.reconstruct_path(
                    came_from,
                    current
                )

            for connection in current.hub.connections:

                neighbor = connection.get_neighbor(
                    current.hub
                )

                if not neighbor.is_traversable():
                    continue
                
                movement_turns = neighbor.movement_cost()
                next_time = (current.timestep + movement_turns)

                if not self.reservation_table.hub_available(
                    neighbor,
                    next_time
                ):
                    continue

                if not self.reservation_table.connection_available(
                    connection,
                    next_time
                ):
                    continue

                neighbor_state = SpaceTimeState(
                    hub=neighbor,
                    timestep=next_time
                )

                edge_cost = cost_model.edge_cost(
                    connection,
                    neighbor,
                    timestep=next_time
                )

                tentative_g = (
                    g_score[current]
                    +
                    edge_cost
                )

                if (
                    neighbor_state not in g_score
                    or
                    tentative_g < g_score[neighbor_state]
                ):

                    g_score[
                        neighbor_state
                    ] = tentative_g

                    came_from[
                        neighbor_state
                    ] = current

                    f_score = (
                        tentative_g
                        +
                        cost_model.heuristic(
                            neighbor,
                            goal
                        )
                    )

                    heapq.heappush(
                        queue,
                        (
                            f_score,
                            neighbor_state
                        )
                    )

        return []

    def reconstruct_path(
        self,
        came_from: dict[SpaceTimeState, SpaceTimeState | None],
        current: SpaceTimeState
    ) -> list[Hub]:

        state_path = super().reconstruct_path(
            came_from,
            current
        )

        return [
            state.hub
            for state in state_path
        ]
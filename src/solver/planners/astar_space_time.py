import heapq
from itertools import count

from ..cost.cost_model import CostModel
from ..simulation.reservation_table import ReservationTable

from ..models import (
    SpaceTimeState,
    EdgeTimeInterval,
)

from ...domain import (
    Hub,
)


class SpaceTimeAStarPlanner():

    def __init__(self, reservation_table: ReservationTable) -> None:
        self.reservation_table = reservation_table

    def plan(
        self,
        start: Hub,
        goal: Hub,
    ) -> list[SpaceTimeState]:

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

        path: list[
            SpaceTimeState
        ] = []

        while current is not None:

            path.append(current)

            current = came_from[current]

        path.reverse()

        return path

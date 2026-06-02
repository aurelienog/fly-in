import heapq
from itertools import count

from .base_planner import BasePlanner

from ..cost.cost_model import CostModel
from ..simulation.reservation_table import ReservationTable

from ..models import (
    SpaceTimeState,
    EdgeTimeState,
    CBSConstraint
)

from ...domain import (
    Drone,
    Hub,
    Connection,
    Network
)


class SpaceTimeAStarPlanner(BasePlanner):

    def __init__(
        self,
        reservation_table: ReservationTable | None = None,
        constraints: set[CBSConstraint] | None = None
    ):

        self.reservation_table = reservation_table

        self.constraints = (
            constraints
            if constraints is not None
            else set()
        )

    def plan(
        self,
        drone: Drone,
        start: Hub,
        goal: Hub,
        network: Network
    ) -> list[SpaceTimeState]:

        cost_model = CostModel()

        counter = count()

        start_state = SpaceTimeState(
            hub=start,
            timestep=0
        )

        g_score: dict[
            SpaceTimeState,
            float
        ] = {
            start_state: 0.0
        }

        came_from: dict[
            SpaceTimeState,
            SpaceTimeState | None
        ] = {
            start_state: None
        }

        queue: list[
            tuple[
                float,
                int,
                SpaceTimeState
            ]
        ] = []

        initial_f = cost_model.heuristic(
            start,
            goal
        )

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

            candidate_moves: list[
                tuple[
                    Hub,
                    Connection | None
                ]
            ] = []

            # normal moves

            for connection in current.hub.connections:

                neighbor = (
                    connection.get_neighbor(
                        current.hub
                    )
                )

                candidate_moves.append(
                    (
                        neighbor,
                        connection
                    )
                )

            # WAIT action

            candidate_moves.append(
                (
                    current.hub,
                    None
                )
            )

            for neighbor, connection in candidate_moves:

                if not neighbor.is_traversable():
                    continue

                if connection is None:

                    movement_turns = 1

                else:

                    movement_turns = (
                        neighbor.movement_cost()
                    )

                next_time = (
                    current.timestep
                    +
                    movement_turns
                )

                if self.is_forbidden(
                    drone,
                    neighbor,
                    connection,
                    next_time
                ):
                    continue

                neighbor_state = SpaceTimeState(
                    hub=neighbor,
                    timestep=next_time
                )

                if self.reservation_table is not None:

                    if not (
                        self.reservation_table
                        .state_available(
                            neighbor_state
                        )
                    ):
                        continue

                    if connection is not None:

                        edge_state = EdgeTimeState(
                            connection=connection,
                            timestep=next_time
                        )

                        if not (
                            self.reservation_table
                            .connection_available(
                                edge_state
                            )
                        ):
                            continue

                if connection is None:

                    edge_cost = 1

                else:

                    edge_cost = (
                        cost_model.edge_cost(
                            connection,
                            neighbor,
                            timestep=next_time
                        )
                    )

                tentative_g = (
                    g_score[current]
                    +
                    edge_cost
                )

                if (
                    neighbor_state not in g_score
                    or
                    tentative_g
                    <
                    g_score[neighbor_state]
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
                            next(counter),
                            neighbor_state
                        )
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

    def is_forbidden(
        self,
        drone: Drone,
        neighbor: Hub,
        connection: Connection | None,
        timestep: int
    ) -> bool:

        for constraint in self.constraints:

            if constraint.drone != drone:
                continue

            if constraint.timestep != timestep:
                continue

            # vertex constraint

            if (
                constraint.hub is not None
                and constraint.hub == neighbor
            ):
                return True

            # edge constraint

            if (
                connection is not None
                and constraint.connection == connection
            ):
                return True

        return False

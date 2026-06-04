from ..models import SpaceTimeState, EdgeTimeInterval
from ...domain import Connection
from collections import defaultdict


class ReservationTable:

    def __init__(self) -> None:

        self.node_reservations: dict[SpaceTimeState, int] = defaultdict(int)
        self.edge_reservations: dict[tuple[Connection, int], int] = defaultdict(int)

    def state_available(self, state: SpaceTimeState) -> bool:

        occupied = self.node_reservations[state]

        return occupied < state.hub.max_drones

    def reserve_state(self, state: SpaceTimeState) -> None:

        self.node_reservations[state] += 1

    def interval_available(self, interval: EdgeTimeInterval) -> bool:

        for t in range(interval.t_start, interval.t_end):

            key = (interval.connection, t)

            if self.edge_reservations[key] >= interval.connection.max_link_capacity:
                return False

        return True

    def reserve_interval(self, interval: EdgeTimeInterval) -> None:
        for t in range(interval.t_start, interval.t_end):

            key = (interval.connection, t)
            self.edge_reservations[key] += 1

    def reserve_path(self, path: list[SpaceTimeState]) -> None:

        for state in path:
            self.reserve_state(state)

        for prev, curr in zip(path, path[1:]):

            if prev.hub == curr.hub:
                continue

            connection = prev.hub.get_connection(curr.hub)

            interval = EdgeTimeInterval(
                connection=connection,
                t_start=prev.timestep,
                t_end=curr.timestep
            )

            self.reserve_interval(interval)

from .models import SpaceTimeState, EdgeTimeInterval
from ..domain import Connection
from collections import defaultdict


class ReservationTable:
    """Manages space-time reservations for nodes and edges in a network.

    The reservation table is used by planning algorithms to ensure that
    multiple agents (e.g., drones) do not conflict in time or space.
    It tracks:

        - Node reservations (hub occupancy over time)
        - Edge reservations (connection usage over time intervals)

    This structure supports space-time pathfinding and collision avoidance
    in multi-agent routing systems.
    """

    def __init__(self) -> None:
        """Initialize an empty reservation table."""

        self.node_reservations: dict[SpaceTimeState, int] = defaultdict(int)
        self.edge_reservations: dict[tuple[Connection, int], int] = defaultdict(int)

    def state_available(self, state: SpaceTimeState) -> bool:
        """Check whether a space-time state is available for reservation.

        Args:
            state: A space-time node state to evaluate.

        Returns:
            True if the state has remaining capacity, False otherwise.
        """

        occupied = self.node_reservations[state]

        return occupied < state.hub.max_drones

    def reserve_state(self, state: SpaceTimeState) -> None:
        """Reserve a node state in time-space.

        Args:
            state: The state to reserve.

        Returns:
            None.
        """

        self.node_reservations[state] += 1

    def interval_available(self, interval: EdgeTimeInterval) -> bool:
        """Check whether a time interval on an edge is available.

        Args:
            interval: The edge-time interval to evaluate.

        Returns:
            True if the interval can be reserved, False otherwise.
        """

        for t in range(interval.t_start, interval.t_end):

            key = (interval.connection, t)

            if self.edge_reservations[key] >= interval.connection.max_link_capacity:
                return False

        return True

    def reserve_interval(self, interval: EdgeTimeInterval) -> None:
        for t in range(interval.t_start, interval.t_end):
            """Reserve a time interval on a connection.

            Args:
                interval: The edge-time interval to reserve.

            Returns:
                None.
            """

            key = (interval.connection, t)
            self.edge_reservations[key] += 1

    def reserve_path(self, path: list[SpaceTimeState]) -> None:
        """Reserve an entire space-time path.

        The method reserves both node states and the transitions between
        them as edge intervals.

        Args:
            path: Ordered list of space-time states representing a path.

        Returns:
            None.
        """

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

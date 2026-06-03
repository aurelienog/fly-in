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

    # def connection_available(
    #         self,
    #         edge_state: EdgeTimeState | None
    #         ) -> bool:
    #     if not edge_state:
    #         return False
    #     occupied = self.edge_reservations[edge_state]

    #     return (occupied < edge_state.connection.max_link_capacity)
    def interval_available(self, interval: EdgeTimeInterval) -> bool:

        for t in range(interval.t_start, interval.t_end):

            key = (interval.connection, t)

            if self.edge_reservations[key] >= interval.connection.max_link_capacity:
                return False

        return True

    # def reserve_connection(
    #     self,
    #     edge_state: EdgeTimeState
    # ) -> None:

    #     self.edge_reservations[edge_state] += 1
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

    # def reserve_path(
    #     self,
    #     path: list[SpaceTimeState]
    # ) -> None:

    #     for state in path:
    #         self.reserve_state(state)

    #     for previous, current in zip(
    #         path,
    #         path[1:]
    #     ):

    #         if previous.hub == current.hub:
    #             continue

    #         connection = (
    #             previous.hub
    #             .get_connection(current.hub)
    #         )

    #         for t in range(
    #             previous.timestep + 1,
    #             current.timestep + 1
    #         ):
    #             edge_state = EdgeTimeState(
    #                 connection=connection,
    #                 timestep=t
    #             )

    #             self.reserve_connection(
    #                 edge_state
    #             )

    # def reserve_path(self, path: list[SpaceTimeState]) -> None:

    #     for i, state in enumerate(path):

    #         self.reserve_state(state)

    #         if i == 0:
    #             continue

    #         previous = path[i - 1]

    #         if previous.hub == state.hub:
    #             continue

    #         connection = (previous.hub.get_connection(state.hub))

    #         edge_state = EdgeTimeState(
    #             connection=connection,
    #             timestep=state.timestep
    #         )
    #         self.reserve_connection(edge_state)


# class ReservationTable:

#     GOAL_HORIZON = 500

#     def __init__(self):

#         self.node_reservations = defaultdict(int)
#         self.edge_reservations = defaultdict(int)

#     def state_available(self, state: SpaceTimeState) -> bool:

#         occupied = self.node_reservations[state]

#         return occupied < state.hub.max_drones

#     def reserve_node(self, state: SpaceTimeState) -> None:

#         self.node_reservations[state] += 1

#     def connection_available(
#             self,
#             edge_state: EdgeTimeState | None
#             ) -> bool:

#         if not edge_state:
#             return False

#         occupied = self.edge_reservations[edge_state]

#         return (occupied < edge_state.connection.max_link_capacity)

#     def reserve_connection(
#         self,
#         edge_state: EdgeTimeState
#     ) -> None:

#         self.edge_reservations[edge_state] += 1

#     def reserve_path(self, path: list[SpaceTimeState]) -> None:

#         for state in path:
#             self.reserve_node(state)

#         for i in range(1, len(path)):

#             previous = path[i - 1]
#             current = path[i]

#             if previous.hub == current.hub:
#                 continue

#             connection = previous.hub.get_connection(current.hub)

#             edge_state = EdgeTimeState(
#                 connection=connection,
#                 timestep=current.timestep
#             )
#             self.reserve_connection(edge_state)

#             goal_state = path[-1]

#             for t in range(goal_state.timestep, self.GOAL_HORIZON):
#                 self.node_reservations[(goal_state.hub, t)] += 1

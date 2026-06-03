from ..models import SpaceTimeState, EdgeTimeState

from collections import defaultdict


class ReservationTable:

    def __init__(self):

        self.node_reservations = defaultdict(int)
        self.edge_reservations = defaultdict(int)

    def state_available(self, state: SpaceTimeState) -> bool:

        occupied = self.node_reservations[state]

        return occupied < state.hub.max_drones

    def reserve_state(self, state: SpaceTimeState) -> None:

        self.node_reservations[state] += 1

    def connection_available(
            self,
            edge_state: EdgeTimeState | None
            ) -> bool:
        if not edge_state:
            return False
        occupied = self.edge_reservations[edge_state]

        return (occupied < edge_state.connection.max_link_capacity)

    def reserve_connection(
        self,
        edge_state: EdgeTimeState
    ) -> None:

        self.edge_reservations[edge_state] += 1

    def reserve_path(self, path: list[SpaceTimeState]) -> None:

        for i, state in enumerate(path):

            self.reserve_state(state)

            if i == 0:
                continue

            previous = path[i - 1]

            if previous.hub == state.hub:
                continue

            connection = (previous.hub.get_connection(state.hub))

            edge_state = EdgeTimeState(
                connection=connection,
                timestep=state.timestep
            )
            self.reserve_connection(edge_state)


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

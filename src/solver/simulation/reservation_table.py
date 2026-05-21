from ...domain import Hub, Connection
from collections import defaultdict


class ReservationTable:

    def __init__(self):

        self.node_reservations = defaultdict(int)
        self.edge_reservations = defaultdict(int)

    def hub_available(self, hub: Hub, timestep: int) -> bool:

        occupied = self.node_reservations[(hub, timestep)]

        return occupied < hub.max_drones

    def reserve_hub(self, hub: Hub, timestep: int) -> None:

        self.node_reservations[(hub, timestep)] += 1

    def connection_available(
            self,
            connection: Connection,
            timestep: int
            ) -> bool:

        occupied = self.edge_reservations[(connection, timestep)]

        return (occupied < connection.max_link_capacity)

    def reserve_connection(
        self,
        connection: Connection,
        timestep: int
    ) -> None:

        self.edge_reservations[(connection, timestep)] += 1

    def reserve_path(self, path: list[Hub]) -> None:

        timestep = 0

        for i, hub in enumerate(path):

            self.reserve_hub(
                hub,
                timestep
            )

            if i > 0:

                previous = path[i - 1]

                connection = (
                    previous
                    .get_connection(hub)
                )

                self.reserve_connection(
                    connection,
                    timestep
                )

            timestep += 1

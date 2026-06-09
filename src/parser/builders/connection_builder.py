from ..models import RawConnection
from ...domain import Connection, Hub


def build_connection(
        raw_connection: RawConnection,
        hub_map: dict[str, Hub]
) -> Connection:

    hub_a = hub_map[raw_connection.a]
    hub_b = hub_map[raw_connection.b]

    connection = Connection(
        hubs=(hub_a, hub_b),
        max_link_capacity=raw_connection.max_link_capacity,
    )

    hub_a.connections.append(connection)
    hub_b.connections.append(connection)

    return Connection(
        hubs=(hub_a, hub_b),
        max_link_capacity=raw_connection.max_link_capacity,
    )

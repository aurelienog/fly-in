from . import RawNetwork
from ..domain import Network, Hub, Connection
from .builders import build_hub, build_connection
from .semantic_layer import validate_network


def build_hub_map(raw: RawNetwork) -> tuple[dict[str, Hub], Hub, Hub]:
    start_hub: Hub | None = None
    end_hub: Hub | None = None
    hub_map: dict[str, Hub] = {}

    for h in raw.hubs:

        hub = build_hub(h)
        hub_map[h.name] = hub

        if h.hub_type == "start_hub":
            start_hub = hub

        elif h.hub_type == "end_hub":
            end_hub = hub

    return hub_map, start_hub, end_hub


def build_network(raw: RawNetwork) -> Network:

    validate_network(raw)

    hub_map, start_hub, end_hub = build_hub_map(raw)

    assert start_hub is not None
    assert end_hub is not None

    connections: list[Connection] = [
        build_connection(raw_connection, hub_map)
        for raw_connection in raw.connections]

    return Network(
        start_hub=start_hub,
        end_hub=end_hub,
        hubs=list(hub_map.values()),
        connections=connections
    )

# def build_network(raw: RawNetwork) -> Network:
#     hub_map: dict[str, Hub] = {}
#     connections: list[Connection] = []

#     seen_connections: set[frozenset[str]] = set()
#     start_hub: Hub | None = None
#     end_hub: Hub | None = None

#     for raw_hub in raw.hubs:

#         hub = build_hub(raw_hub)

#         if hub.name in hub_map:
#             raise DomainError(
#                 f"duplicate hub name: {hub.name}"
#             )

#         if raw_hub.hub_type == "start_hub":

#             if start_hub is not None:
#                 raise DomainError(
#                     "multiple start hubs"
#                 )
#             start_hub = hub

#         elif raw_hub.hub_type == "end_hub":

#             if end_hub is not None:
#                 raise DomainError(
#                     "multiple end hubs"
#                 )
#             end_hub = hub

#         hub_map[hub.name] = hub

#     for raw_connection in raw.connections:
#         key = frozenset({
#                 raw_connection.a,
#                 raw_connection.b,
#             })

#         if key in seen_connections:
#             raise DomainError(
#                 f"duplicate connection: "
#                 f"{raw_connection.a}-{raw_connection.b}"
#             )

#         seen_connections.add(key)

#         connection = build_connection(raw_connection, hub_map)
#         connections.append(connection)

#     if start_hub is None:
#         raise DomainError("missing start hub")

#     if end_hub is None:
#         raise DomainError("missing end hub")

#     return Network(
#         start_hub=start_hub,
#         end_hub=end_hub,
#         hubs=list(hub_map.values()),
#         connections=connections
#     )

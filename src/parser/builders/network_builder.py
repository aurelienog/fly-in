from ..models import RawNetwork
from ...domain import Network, Hub, Connection
from .hub_builder import build_hub
from .connection_builder import build_connection


def build_hub_map(raw: RawNetwork) -> tuple[dict[str, Hub], Hub | None, Hub | None]:
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

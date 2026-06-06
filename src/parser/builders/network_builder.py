from ..models import RawNetwork
from ...domain import Network, Hub, Connection, HubRole
from .hub_builder import build_hub
from .connection_builder import build_connection
from ...errors import SemanticError


def build_hub_map(raw: RawNetwork) -> tuple[dict[str, Hub], Hub | None, Hub | None]:
    start_hub: Hub | None = None
    end_hub: Hub | None = None
    hub_map: dict[str, Hub] = {}

    for h in raw.hubs:

        hub = build_hub(h)
        hub_map[h.name] = hub

        if h.hub_type == HubRole.START.value:
            start_hub = hub

        elif h.hub_type == HubRole.END.value:
            end_hub = hub

    return hub_map, start_hub, end_hub


def build_network(raw: RawNetwork) -> Network:

    hub_map, start_hub, end_hub = build_hub_map(raw)

    if start_hub is None or end_hub is None:
        raise SemanticError("Invalid network: missing start or end hub")

    connections: list[Connection] = [
        build_connection(raw_connection, hub_map)
        for raw_connection in raw.connections]

    return Network(
        start_hub=start_hub,
        end_hub=end_hub,
        hubs=list(hub_map.values()),
        connections=connections
    )

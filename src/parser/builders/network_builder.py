from ..models import RawNetwork
from ...domain import Network, Hub, Connection, HubRole
from .hub_builder import build_hub
from .connection_builder import build_connection
from ...errors import SemanticError


def build_hub_map(raw: RawNetwork) -> tuple[dict[str, Hub], Hub | None, Hub | None]:
    """Create hubs from a raw network description and index them by name.

    While building the mapping, the function also identifies the start
    and end hubs defined in the network.

    Args:
        raw: Raw network data containing hub definitions.

    Returns:
        A tuple containing:
            - A mapping from hub names to hub instances.
            - The start hub, or ``None`` if no start hub is defined.
            - The end hub, or ``None`` if no end hub is defined.
    """
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
    """Build a complete network from its raw representation.

    The function creates all hubs and connections and validates that
    both a start hub and an end hub are defined.

    Args:
        raw: Raw network data describing hubs and connections.

    Returns:
        The constructed network.

    Raises:
        SemanticError: If the network does not define a start hub or an
            end hub.
    """

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

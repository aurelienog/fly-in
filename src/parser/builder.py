from . import RawNetwork
from ..domain import Network, Hub, Connection
from dataclasses import asdict


def build_network(raw: RawNetwork) -> Network:
    connections: list[Connection] = []
    hubs: list[Hub] = []

    start_hub = None
    end_hub = None

    for hub in raw.hubs:
        data = asdict(hub)
        if hub.hub_type == "start_hub":
            start_hub = Hub(**data)

        elif hub.hub_type == "end_hub":
            end_hub = Hub(**data)

        elif hub.hub_type == "hub":
            hubs.append(Hub(**data))

    for connection in raw.connections:
        #aqui se debe convertir los str a y b -> Hub
        #max link =
        #occupation =
        connections.append(Connection())

    return Network(
        start_hub,
        end_hub,
        hubs,
        connections,
    )

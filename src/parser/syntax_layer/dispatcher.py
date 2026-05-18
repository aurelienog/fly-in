from .drones_number_parser import parse_nb_drones
from .connection_parser import parse_connection
from .hub_parser import parse_hub
from ...errors import ParseError
from ..models import RawNetwork, RawHub, RawConnection


def parse_network(tokens: list[tuple[int, str, str]]) -> RawNetwork:

    hubs: list[RawHub] = []
    connections: list[RawConnection] = []
    nb_drones: int = 0

    hub_keywords = {"hub", "start_hub", "end_hub"}

    for line, keyword, content in tokens:
        if keyword in hub_keywords:
            hubs.append(parse_hub(content, keyword))

        elif keyword == "connection":
            connections.append(parse_connection(content))

        elif keyword == "nb_drones":
            nb_drones = parse_nb_drones(content)

        else:
            raise ParseError(f"Line {line}: unknown keyword {keyword}")

    return RawNetwork(nb_drones, hubs, connections)

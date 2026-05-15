from .syntax_layer import parse_nb_drones, parse_connection, parse_hub
from ..errors import ParseError
from .models import RawNetwork


def parse_network(tokens: list[tuple[int, str, str]]) -> RawNetwork:

    hubs: list = []
    connections: list = []
    nb_drones: int = 0

    valid_hubs = {"hub", "start_hub", "end_hub"}

    for line, keyword, content in tokens:
        if keyword in valid_hubs:
            hubs.append(parse_hub(content, keyword))

        elif keyword == "connection":
            connections.append(parse_connection(content))

        elif keyword == "nb_drones":
            nb_drones = parse_nb_drones(content)

        else:
            raise ParseError(f"Line {line}: unknown keyword {keyword}")

    return RawNetwork(nb_drones, hubs, connections)

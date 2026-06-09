from .drones_number_parser import parse_nb_drones
from .connection_parser import parse_connection
from .hub_parser import parse_hub
from ...errors import ParseError
from ..models import RawNetwork, RawHub, RawConnection


def parse_raw_network(tokens: list[tuple[int, str, str]]) -> RawNetwork:

    hubs: list[RawHub] = []
    connections: list[RawConnection] = []
    nb_drones: int = 0

    hub_keywords = {"hub", "start_hub", "end_hub"}

    if not tokens:
        raise ParseError("empty file")

    first_line, first_keyword, first_content = tokens[0]
    if first_keyword != "nb_drones":
        raise ParseError(f"line {first_line}: "
                         "first line must define nb_drones")

    nb_drones = parse_nb_drones(first_content, first_line)

    for line, keyword, content in tokens[1:]:
        if keyword in hub_keywords:
            hubs.append(parse_hub(content, keyword, line))

        elif keyword == "connection":
            connections.append(parse_connection(content, line))

        elif keyword == "nb_drones":
            raise ParseError(f"Line {line}: duplicated keyword {keyword}")

        else:
            raise ParseError(f"Line {line}: unknown keyword {keyword}")

    return RawNetwork(nb_drones, hubs, connections)

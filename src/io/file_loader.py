from ..domain import Network
from ..parser import parse_network


def load_network(path: str) -> Network:

    with open(path, "r", encoding="utf8") as file:
        source = file.read()
    return parse_network(source)

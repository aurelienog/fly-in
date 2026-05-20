from ..domain import Network
from ..parser import parse_network
from pathlib import Path


def load_network(path: Path) -> Network:

    with path.open(encoding="utf8") as file:
        source = file.read()
    return parse_network(source)

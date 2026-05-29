from ..domain import Network
from ..parser import parse_simulation
from pathlib import Path


def load_simulation(path: str) -> Network:
    path = Path(path)
    with path.open(encoding="utf8") as file:
        source = file.read()
    return parse_simulation(source)

from ..domain import Network, Drone
from ..parser import parse_simulation
from pathlib import Path


def load_simulation(content: str) -> tuple[Network, list[Drone]]:
    path = Path(content)
    with path.open(encoding="utf8") as file:
        source = file.read()
    return parse_simulation(source)

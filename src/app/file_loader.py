from ..domain import Network, Drone
from ..parser import parse_simulation
from pathlib import Path


def load_simulation(content: str) -> tuple[Network, list[Drone]]:
    """Load a simulation definition from a file and parse its contents.

    Args:
        content: Path to the file containing the simulation definition.

    Returns:
        A tuple containing the parsed network and the list of drones
        defined in the simulation.
    """
    path = Path(content)
    with path.open(encoding="utf8") as file:
        source = file.read()
    return parse_simulation(source)

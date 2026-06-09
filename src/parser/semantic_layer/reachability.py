from ...domain import Network, Hub
from ...errors import SimulationError

from collections import deque


def has_path(network: Network) -> bool:
    """Determine whether a traversable path exists in the network.

    The search is performed from the start hub to the end hub while
    ignoring hubs that are not traversable.

    Args:
        network: Network to analyze.

    Returns:
        True if a path exists between the start and end hubs, False
        otherwise.
    """
    start = network.start_hub

    queue: deque[Hub] = deque([start])
    visited: set[Hub] = {start}

    while queue:
        current = queue.popleft()

        if current == network.end_hub:
            return True

        for connection in current.connections:
            neighbor = connection.get_neighbor(current)

            if not neighbor.is_traversable():
                continue

            if neighbor in visited:
                continue

            visited.add(neighbor)
            queue.append(neighbor)

    return False


def validate_reachability(network: Network) -> None:

    """Validate that the network contains a traversable path.

    The validation ensures that the end hub can be reached from the
    start hub.

    Args:
        network: Network to validate.

    Raises:
        SimulationError: If no traversable path exists between the start
            and end hubs.
    """
    if not has_path(network):
        raise SimulationError(f"No path between '{network.start_hub.name}'"
                              f" and '{network.end_hub.name}'")

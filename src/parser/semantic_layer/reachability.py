from ...domain import Network, Hub
from ...errors import SimulationError

from collections import deque


def has_path(network: Network) -> bool:
    start = network.start_hub

    queue: deque[Hub] = [start]
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
    if not has_path(network):
        raise SimulationError(f"No path between '{network.start_hub.name}'"
                              f" and '{network.end_hub.name}'")

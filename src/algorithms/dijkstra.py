from ..domain import Hub, Network, Connection
from collections import deque
import math


def dijkstra(current_hub: Hub, target: Hub, network: Network) -> list[Hub]:
    path = []
    progress: dict[str, tuple(Hub, int, Hub | None)]= []    # node | cost | previous
    queue: deque[Hub] = deque()
    queue.append(current_hub)

    # initialize
    for hub in network.hubs:

        if hub == current_hub:
            progress[hub.name] = (hub, 0, None)
        else:
            progress[hub.name] = (hub, math.inf, None)

    while queue is not None:
        current = queue.popleft()
        current_cost = progress[current.name][1]

        for connection in current.connections:

            neighbor = connection.get_neighbor(current) # need to check priority?

            if not neighbor.is_traversable():
                continue

            new_cost = current_cost + neighbor.movement_cost()
            if new_cost < progress[neighbor.name]:
                progress[neighbor.name] = (neighbor, new_cost, current)
            connection.occupation += 1
            queue.append(neighbor)

    return path



# occupancy
# capacities

# priority a agregar

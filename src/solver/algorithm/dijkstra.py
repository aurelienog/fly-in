from ...domain import Hub, Network
from ..cost.cost_model import CostModel

import heapq
import math


def dijkstra(
        current_hub: Hub,
        target: Hub,
        network: Network
) -> list[Hub]:

    progress: dict[Hub, tuple[float, Hub | None]] = {}

    cost_model = CostModel()

    for hub in network.hubs:

        if hub == current_hub:
            progress[hub] = (0, None)
        else:
            progress[hub] = (math.inf, None)

    queue = []

    heapq.heappush(
        queue,
        (0, current_hub)
    )

    while queue:

        priority, current = heapq.heappop(queue)

        if priority > progress[current][0]:
            continue

        if current == target:
            break

        current_cost = progress[current][0]

        for connection in current.connections:

            neighbor = connection.get_neighbor(current)

            if not neighbor.is_traversable():
                continue

            edge_cost = cost_model.edge_cost(
                connection, neighbor
            )

            new_cost = current_cost + edge_cost

            if new_cost < progress[neighbor][0]:

                progress[neighbor] = (
                    new_cost,
                    current
                )

                heapq.heappush(
                    queue,
                    (new_cost, neighbor)
                )

    path = []

    current = target

    while current is not None:

        path.append(current)

        current = progress[current][1]

    path.reverse()

    return path


"""
current hub
    ↓
connection.get_neighbor(current)
    ↓
neighbor

CostModel.edge_cost(
    connection,
    neighbor
)
    ↓
connection.get_cost(neighbor)
    ↓
static map cost
"""

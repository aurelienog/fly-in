import heapq
import math

from .base_planner import BasePlanner
from ..cost.cost_model import CostModel
from ...domain import Hub, Network


class DijkstraPlanner(BasePlanner):

    def plan(
        self,
        start: Hub,
        goal: Hub,
        network: Network
    ) -> list[Hub]:

        cost_model = CostModel()

        g_score: dict[Hub, float] = {
            hub: math.inf
            for hub in network.hubs
        }

        came_from: dict[Hub, Hub | None] = {
            start: None
        }

        g_score[start] = 0

        queue: list[tuple[int, Hub]] = []

        heapq.heappush(
            queue,
            (0, start)
        )

        while queue:

            priority, current = heapq.heappop(queue)

            # ignore stale entries
            if priority > g_score[current]:
                continue

            if current == goal:

                return self.reconstruct_path(
                    came_from,
                    goal
                )

            for connection in current.connections:

                neighbor = connection.get_neighbor(
                    current
                )

                if not neighbor.is_traversable():
                    continue

                edge_cost = cost_model.edge_cost(
                    connection,
                    neighbor
                )

                tentative_g = (
                    g_score[current]
                    + edge_cost
                )

                if tentative_g < g_score[neighbor]:

                    g_score[neighbor] = tentative_g

                    came_from[neighbor] = current

                    heapq.heappush(
                        queue,
                        (
                            tentative_g,
                            neighbor
                        )
                    )

        return []


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

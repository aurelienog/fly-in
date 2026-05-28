from src.solver.planners import DijkstraPlanner
from src.tests.helpers.network import build_linear_network, build_multiple_path_network
from src.domain import Network, Hub, HubRole, ZoneType

import pytest


@pytest.mark.parametrize(
    "size",
    [2, 3, 5, 10]
)
def test_linear_network(size):

    planner = DijkstraPlanner()
    network, hubs = build_linear_network(size)

    path = planner.plan(
        network.start_hub,
        network.end_hub,
        network
    )

    assert path == hubs


def test_returns_empty_when_no_path():

    planner = DijkstraPlanner()
    a = Hub("start", (0, 0), HubRole.START, max_drones=2)
    b = Hub("goal", (3, 0), HubRole.END, max_drones=2)
    network = Network(a, b, [a, b], [])

    path = planner.plan(a, b, network)

    assert path == []


@pytest.mark.parametrize(
    "size",
    [3, 5, 10]
)
def test_ignores_non_traversable_nodes(size):

    planner = DijkstraPlanner()
    network, hubs = build_linear_network(size)
    hubs[2].zone = ZoneType.BLOCKED

    path = planner.plan(network.start_hub, network.end_hub, network)

    assert path == []


def test_chooses_lowest_cost_path():

    planner = DijkstraPlanner()
    start, cheap_1, cheap_2, expensive, goal, network = build_multiple_path_network()

    path = planner.plan(network.start_hub, network.end_hub, network)

    assert path == [start, cheap_1, cheap_2, goal]
    assert len(path) == 4


def test_start_equals_goal():

    planner = DijkstraPlanner()
    network, _ = build_linear_network(1)

    path = planner.plan(network.start_hub, network.end_hub, network)

    assert path == [network.start_hub]


# def test_revisits_node_with_lower_cost()
# if priority > g_score[current]:
#     continue

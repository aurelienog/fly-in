from src.domain import Network, Hub, Connection, HubRole


def connect(a: Hub, b: Hub) -> Connection:

    connection = Connection((a, b))

    a.connections.append(connection)
    b.connections.append(connection)

    return connection


def build_linear_network(size: int):

    hubs = []

    for i in range(size):

        role = HubRole.HUB

        if i == 0:
            role = HubRole.START
            max_drones = size

        elif i == size - 1:
            role = HubRole.END
            max_drones = size
        else:
            max_drones = 1
        hubs.append(
            Hub(f"hub_{i}", (i, 0), role, max_drones=max_drones)
        )

    connections = []

    for i in range(size - 1):

        connections.append(connect(
                hubs[i],
                hubs[i + 1]
            ))

    network = Network(
        hubs[0],
        hubs[-1],
        hubs,
        connections
    )

    return network, hubs


def build_multiple_path_network():
    start = Hub(
        "start",
        (0, 0),
        HubRole.START,
        max_drones=4
    )

    cheap_1 = Hub(
        "cheap_1",
        (1, 0),
        HubRole.HUB,
        max_drones=1
    )

    cheap_2 = Hub(
        "cheap_2",
        (2, 0),
        HubRole.HUB,
        max_drones=1
    )

    expensive = Hub(
        "expensive",
        (1, 1),
        HubRole.HUB,
        max_drones=100
    )

    goal = Hub(
        "goal",
        (3, 0),
        HubRole.END,
        max_drones=4
    )

    connections = [
        connect(start, cheap_1),
        connect(cheap_1, cheap_2),
        connect(cheap_2, goal),

        connect(start, expensive),
        connect(expensive, goal),
    ]

    network = Network(
        start,
        goal,
        [
            start,
            cheap_1,
            cheap_2,
            expensive,
            goal
        ],
        connections
    )

    return start, cheap_1, cheap_2, expensive, goal, network

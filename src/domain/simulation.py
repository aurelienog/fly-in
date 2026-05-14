from ..domain import Network, Connection


class Simulation:
    def __init__(self, network: Network) -> None:
        self.drones = []
        self.network = network
        self.connections: list[Connection] = []

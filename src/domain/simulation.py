from ..domain import Network, Connection, Drone


class Simulation:
    def __init__(self, network: Network) -> None:
        self.drones: list[Drone] = []
        self.network = network
        self.connections: list[Connection] = []

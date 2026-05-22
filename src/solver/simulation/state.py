from dataclasses import dataclass
from ...domain import Network, Drone


@dataclass
class State:
    drones: Drone
    network: Network
    time: int
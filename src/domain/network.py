from .hub import Hub
from .connection import Connection
from dataclasses import dataclass


@dataclass
class Network():
    """Represents the complete network topology.

    Attributes:
        start_hub: The designated starting hub of the network.
        end_hub: The designated destination hub of the network.
        hubs: All hubs that belong to the network.
        connections: All connections linking the hubs.
    """
    start_hub: Hub
    end_hub: Hub
    hubs: list[Hub]
    connections: list[Connection]

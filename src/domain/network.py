from .hub import Hub
from .connection import Connection
from dataclasses import dataclass


@dataclass
class Network():
    start_hub: Hub
    end_hub: Hub
    hubs: list[Hub]
    connections: list[Connection]

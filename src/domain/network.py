from . import Connection


class Network():
    def __init__(self, start_hub, end_hub, hubs, connections) -> None:
        self.start_hub = start_hub
        self.end_hub = end_hub
        self.hubs = hubs
        self.connections: list[Connection] = connections

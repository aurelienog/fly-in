from ..domain import Connection


class Graph():
    def __init__(self, start_hub, end_hub) -> None:
        self.start_hub = start_hub
        self.end_hub = end_hub
        self.hubs = {}
        self.connections: list[Connection] = []

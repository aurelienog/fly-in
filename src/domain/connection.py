from ..models import Hub


class Connection():
    def __init__(self, hub1: Hub, hub2: Hub, max_link_capacity: int) -> None:
        self.max_link_capacity: int = max_link_capacity
        self.occupation: int = 0
        self.hubs: tuple[Hub, Hub] = (hub1, hub2)

from enum import Enum


class HubType(Enum):
    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"


class Hub:
    def __init__(self, name: str,
                 position: tuple[int, int],
                 max_drones: int = 1,
                 hub_type: HubType = HubType.NORMAL,
                 color: str = "default",
                 ) -> None:
        self.name: str = name
        self.max_drones: int = max_drones
        self.color = color
        self.hub_type = hub_type
        self.position = position

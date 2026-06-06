from dataclasses import dataclass
from ..domain import Color


@dataclass
class RawHub:

    line: int

    hub_type: str
    name: str
    x: int
    y: int

    zone: str = "normal"
    color: Color = Color.DEFAULT
    max_drones: int = 1


@dataclass
class RawConnection:

    line: int

    a: str
    b: str
    max_link_capacity: int = 1


@dataclass
class RawNetwork:
    nb_drones: int
    hubs: list[RawHub]
    connections: list[RawConnection]

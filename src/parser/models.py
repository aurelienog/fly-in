from dataclasses import dataclass


@dataclass
class RawHub:

    line: int

    hub_type: str
    name: str
    x: int
    y: int

    zone: str = "normal"
    color: str | None = None
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

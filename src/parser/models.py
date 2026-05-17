from dataclasses import dataclass


@dataclass
class RawHub:
    hub_type: str
    name: str
    x: str
    y: str

    zone: str = "normal"
    color: str | None = None
    max_drones: int = 1


@dataclass
class RawConnection:
    a: str
    b: str
    max_link_capacity: int = 1


@dataclass
class RawNetwork:
    nb_drones: int
    hubs: list[RawHub]
    connections: list[RawConnection]

from dataclasses import dataclass


@dataclass
class RawHub:
    hub_type: str
    name: str
    x: str
    y: str
    metadata: str | None = None


@dataclass
class RawConnection:
    a: str
    b: str
    metadata: str | None = None


@dataclass
class RawNetwork:
    nb_drones: int
    hubs: list[RawHub]
    connections: list[RawConnection]

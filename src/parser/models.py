from dataclasses import dataclass
from ..domain import Color


@dataclass
class RawHub:
    """Raw representation of a hub before validation and normalization.

    Attributes:
        line: Line number in the source file where the hub is defined.
        hub_type: Type of hub (e.g., start, end, or regular hub).
        name: Unique identifier of the hub.
        x: X coordinate of the hub position.
        y: Y coordinate of the hub position.
        zone: Zone classification as raw string (default: "normal").
        color: Display color (default: Color.DEFAULT).
        max_drones: Maximum number of drones allowed in the hub.
    """

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
    """Raw representation of a connection before validation.

    Attributes:
        line: Line number in the source file where the connection is defined.
        a: Name of the first endpoint hub.
        b: Name of the second endpoint hub.
        max_link_capacity: Maximum number of simultaneous traversals allowed.
    """

    line: int

    a: str
    b: str
    max_link_capacity: int = 1


@dataclass
class RawNetwork:
    """Raw representation of a full network before parsing and validation.

    Attributes:
        nb_drones: Number of drones to simulate.
        hubs: List of raw hub definitions.
        connections: List of raw connection definitions.
    """

    nb_drones: int
    hubs: list[RawHub]
    connections: list[RawConnection]

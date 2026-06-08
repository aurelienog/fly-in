from dataclasses import dataclass
from ...domain import Connection


@dataclass(frozen=True)
class EdgeTimeInterval:
    """Represents a time interval during which a connection is traversed.

    This structure models the temporal usage of a network connection in
    a space-time reservation system. It is used to reserve and validate
    edge occupancy over discrete simulation timesteps.

    Attributes:
        connection: The network connection being used.
        t_start: Inclusive start timestep of the traversal.
        t_end: Exclusive end timestep of the traversal.
    """
    connection: Connection
    t_start: int
    t_end: int

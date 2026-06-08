from dataclasses import dataclass
from ..domain import Hub, Connection


@dataclass(frozen=True)
class State:
    """Base class representing a time-dependent simulation state.

    Attributes:
        timestep: Discrete simulation time step at which the state occurs.
    """
    timestep: int


@dataclass(frozen=True)
class HubState(State):
    """Represents the state of a drone located at a hub.

    Attributes:
        timestep: Simulation time step.
        hub: The hub where the drone is located.
    """
    hub: Hub


@dataclass(frozen=True)
class ConnectionState(State):
    """Represents the state of a drone traversing a connection.

    This state describes a drone in transit between two hubs along a
    connection, including its progress along the edge.

    Attributes:
        timestep: Simulation time step.
        connection: The connection being traversed.
        from_hub: Origin hub of the traversal.
        to_hub: Destination hub of the traversal.
        progress: Normalized progress of traversal in the range [0, 1].
    """
    connection: Connection
    timestep: int
    from_hub: Hub
    to_hub: Hub
    progress: float

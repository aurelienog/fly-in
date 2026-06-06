from dataclasses import dataclass
from ..domain import Hub, Connection


@dataclass(frozen=True)
class State:
    timestep: int


@dataclass(frozen=True)
class HubState(State):
    hub: Hub


@dataclass(frozen=True)
class ConnectionState(State):
    connection: Connection
    timestep: int
    from_hub: Hub
    to_hub: Hub
    progress: float

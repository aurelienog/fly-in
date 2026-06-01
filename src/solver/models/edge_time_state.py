from dataclasses import dataclass
from ...domain import Connection


@dataclass(frozen=True)
class EdgeTimeState:

    connection: Connection
    timestep: int

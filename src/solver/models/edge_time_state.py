from dataclasses import dataclass
from ...domain import Connection


@dataclass(frozen=True)
class EdgeTimeInterval:
    connection: Connection
    t_start: int
    t_end: int

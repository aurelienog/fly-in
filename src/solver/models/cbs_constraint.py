from dataclasses import dataclass

from ...domain import Hub, Connection, Drone


@dataclass(frozen=True)
class CBSConstraint:

    drone: Drone

    hub: Hub | None = None

    connection: Connection | None = None

    timestep: int = 0

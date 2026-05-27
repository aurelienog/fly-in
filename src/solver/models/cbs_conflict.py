from dataclasses import dataclass

from ...domain import Drone, Hub, Connection


@dataclass(frozen=True)
class CBSConflict:

    drone1: Drone
    drone2: Drone

    timestep: int

    hub: Hub | None = None
    connection: Connection | None = None

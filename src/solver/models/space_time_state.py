from dataclasses import dataclass
from ...domain import Hub


@dataclass(frozen=True)
class SpaceTimeState:

    hub: Hub

    timestep: int
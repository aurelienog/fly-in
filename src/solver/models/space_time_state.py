from dataclasses import dataclass
from ...domain import Hub


@dataclass(frozen=True)
class SpaceTimeState:
    """Represents the presence of an agent at a hub at a specific timestep.

    This structure is used in space-time planning algorithms to model
    node occupancy over time. It is a fundamental unit for reservation
    systems and multi-agent pathfinding.

    Attributes:
        hub: The hub where the agent is located.
        timestep: The discrete simulation time at which the agent occupies
            the hub.
    """
    hub: Hub
    timestep: int

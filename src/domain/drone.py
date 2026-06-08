from .hub import Hub
from dataclasses import dataclass


@dataclass
class Drone:
    """Represents a drone that must travel through the network.

    Attributes:
        id: Unique identifier of the drone.
        current_hub: Hub where the drone starts.
        target_hub: Destination hub that the drone must reach.
    """
    id: str
    current_hub: Hub
    target_hub: Hub

    def __hash__(self) -> int:
        """Return a hash value for the drone.

        Returns:
            A hash based on the drone's unique identifier.
        """
        return hash(self.id)

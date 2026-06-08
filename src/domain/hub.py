from __future__ import annotations
from .colors import Color
from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .connection import Connection


class ZoneType(Enum):
    """Defines the traversal characteristics of a hub.

    Zone types affect whether a hub can be traversed and may modify the
    cost of moving through the network.
    """
    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"


class HubRole(Enum):
    """Defines the functional role of a hub within the network."""
    HUB = "hub"
    START = "start_hub"
    END = "end_hub"


@dataclass
class Hub:
    """Represents a node in the network.

    Attributes:
        name: Unique name of the hub.
        position: Coordinates of the hub in the network.
        role: Functional role of the hub.
        zone: Zone classification that affects traversal behavior.
        max_drones: Maximum number of drones allowed at the hub.
        color: Display color used for visualization.
        connections: Connections linking this hub to neighboring hubs.
    """
    name: str
    position: tuple[int, int]
    role: HubRole
    zone: ZoneType = ZoneType.NORMAL
    max_drones: int = 1
    color: Color = Color.DEFAULT
    connections: list[Connection] = field(default_factory=list)

    def movement_cost(self) -> int:
        """Return the movement cost associated with this hub.

        Returns:
            The traversal cost modifier for the hub. Restricted hubs
            have a cost of 2, while all other traversable hubs have a
            cost of 1.
        """
        if self.zone is ZoneType.RESTRICTED:
            return 2
        return 1

    def is_traversable(self) -> bool:
        """Determine whether the hub can be traversed.

        Returns:
            True if the hub is traversable, False if it is blocked.
        """
        return self.zone is not ZoneType.BLOCKED

    def is_priority(self) -> bool:
        """Determine whether the hub is marked as a priority hub.

        Returns:
            True if the hub belongs to a priority zone, False otherwise.
        """
        return self.zone is ZoneType.PRIORITY

    def get_connection(self, hub: Hub) -> Connection:
        """Return the connection linking this hub to another hub.

        Args:
            hub: The neighboring hub to search for.

        Returns:
            The connection between this hub and the specified hub.

        Raises:
            ValueError: If no connection exists between the two hubs.
        """
        for connection in self.connections:

            if (connection.get_neighbor(self) == hub):
                return connection

        raise ValueError(
            f"No connection between "
            f"{self.name} and {hub.name}"
        )

    def __hash__(self) -> int:
        """Return a hash value for the hub.

        Returns:
            A hash based on the hub name.
        """
        return hash(self.name)

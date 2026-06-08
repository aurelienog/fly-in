import math
from .hub import Hub, ZoneType
from dataclasses import dataclass


@dataclass
class Connection:
    """Represents a bidirectional connection between two hubs.

    Attributes:
        hubs: Pair of hubs connected by this connection.
        max_link_capacity: Maximum number of simultaneous traversals
            allowed on the connection.
        occupation: Current number of traversals occupying the
            connection.
        base_cost: Optional predefined traversal cost.
    """
    hubs: tuple[Hub, Hub]
    max_link_capacity: int = 1
    occupation: int = 0
    base_cost: float | None = None

    def get_neighbor(self, hub) -> Hub:
        """Return the hub connected to the given hub.

        Args:
            hub: One of the hubs that belongs to this connection.

        Returns:
            The hub at the opposite end of the connection.

        Raises:
            ValueError: If the provided hub is not part of this connection.
        """
        if self.hubs[0] == hub:
            return self.hubs[1]
        elif self.hubs[1] == hub:
            return self.hubs[0]
        else:
            raise ValueError("hub not in connection")

    def is_available(self) -> bool:
        """Check whether the connection can accept additional traffic.

        Returns:
            True if the connection has remaining capacity, False otherwise.
        """
        return self.occupation != self.max_link_capacity

    def remaining_capacity(self) -> int:
        """Return the unused capacity of the connection.

        Returns:
            The number of additional units that can traverse the connection.
        """
        return self.max_link_capacity - self.occupation

    def get_distance(self) -> float:
        """Compute the Euclidean distance between the connected hubs.

        Returns:
            The Euclidean distance between the two hubs.
        """
        hub1, hub2 = self.hubs

        dx = hub1.position[0] - hub2.position[0]
        dy = hub1.position[1] - hub2.position[1]

        return math.sqrt(dx*dx + dy*dy)

    def get_cost(self, destination: Hub):
        """Calculate the static traversal cost of the connection.

        The returned cost is independent of the current simulation state
        and is based on the geometric distance and destination zone
        modifiers.

        Includes:
            - Geometric distance.
            - Zone movement modifiers.
            - Structural penalties.

        Does not include:
            - Congestion.
            - Reservations.
            - Occupancy.
            - Time-dependent costs.

        Args:
            destination: The destination hub reached through this
                connection.

        Returns:
            The traversal cost. Returns ``math.inf`` if the destination
            hub belongs to a blocked zone.
        """

        cost = self.get_distance()

        if destination.zone == ZoneType.BLOCKED:
            return math.inf

        if destination.zone == ZoneType.RESTRICTED:
            cost += 2

        elif destination.zone == ZoneType.PRIORITY:
            cost -= 0.1

        return max(1, cost)

    def __hash__(self) -> int:
        """Return a hash value for the connection.

        Returns:
            A hash based on the pair of connected hubs, independent of
            their order.
        """
        return hash(
            frozenset(self.hubs)
        )

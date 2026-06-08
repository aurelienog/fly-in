from ...domain import Drone, Network
from ..models import RawNetwork


def build_drones(
    raw: RawNetwork,
    network: Network
) -> list[Drone]:
    """Create the drones defined in a raw network description.

    Each drone is initialized at the network's start hub and assigned
    the network's end hub as its destination.

    Args:
        raw: Raw network data containing the number of drones to create.
        network: Network in which the drones will operate.

    Returns:
        A list of initialized drones.
    """

    drones: list[Drone] = []

    for i in range(raw.nb_drones):

        drones.append(

            Drone(
                id=f"D{i}",
                current_hub=network.start_hub,
                target_hub=network.end_hub
            )

        )

    return drones

from ...domain import Drone, Network
from ..models import RawNetwork


def build_drones(
    raw: RawNetwork,
    network: Network
) -> list[Drone]:

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
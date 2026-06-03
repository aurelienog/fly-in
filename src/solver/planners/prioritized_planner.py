from .astar_space_time import (
    SpaceTimeAStarPlanner
)

from ..simulation.reservation_table import (
    ReservationTable
)

from ...domain import (
    Drone,
    Network
)


class PrioritizedPlanner():

    def plan(
        self,
        drones: list[Drone],
        network: Network
    ):

        reservation_table = (
            ReservationTable()
        )

        solution = {}

        #
        # longest routes first
        #

        ordered = sorted(
            drones,
            key=lambda d:
            abs(
                d.current_hub.position[0]
                -
                d.target_hub.position[0]
            )
            +
            abs(
                d.current_hub.position[1]
                -
                d.target_hub.position[1]
            ),
            reverse=True
        )

        for drone in ordered:

            planner = (
                SpaceTimeAStarPlanner(reservation_table)
            )

            path = planner.plan(
                drone,
                drone.current_hub,
                drone.target_hub,
                network
            )

            if not path:

                print(
                    "NO PATH",
                    drone.id
                )

                return {}

            reservation_table.reserve_path(
                path
            )

            solution[
                drone
            ] = path

        return solution

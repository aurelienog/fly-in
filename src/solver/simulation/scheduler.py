from dataclasses import dataclass

from ...domain import Drone, Network
from .reservation_table import ReservationTable
from ..models import SpaceTimeState
from ..planners import SpaceTimeAStarPlanner


@dataclass
class Scheduler:

    planner: SpaceTimeAStarPlanner

    reservation_table: ReservationTable

    def schedule(
        self,
        drones: list[Drone],
        network: Network
    ) -> dict[Drone,  list[SpaceTimeState]]:

        planner = self.planner

        solution: dict[Drone, list[SpaceTimeState]] = {}

        for drone in drones:

            path = planner.plan(
                drone.current_hub,
                drone.target_hub,
            )
            solution[drone] = path
            self.reservation_table.reserve_path(path)

        return solution

# tick()
# move drones
# update occupancy
# release reservations

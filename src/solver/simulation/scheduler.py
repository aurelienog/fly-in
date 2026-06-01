from dataclasses import dataclass

from ...domain import Drone, Network
from ..planners.base_multi_planner import BaseMultiPlanner
from ..planners.base_planner import BasePlanner
from .reservation_table import ReservationTable
from ..models import SpaceTimeState


@dataclass
class Scheduler:

    planner: BasePlanner | BaseMultiPlanner

    reservation_table: ReservationTable

    def schedule(
        self,
        drones: list[Drone],
        network: Network
    ) -> dict[Drone,  list[SpaceTimeState]]:

        planner = self.planner

        if isinstance(
          planner,
          BaseMultiPlanner
        ):
            return planner.plan(drones, network)

        solution: dict[Drone, list[SpaceTimeState]] = {}

        for drone in drones:

            path = planner.plan(
                drone,
                drone.current_hub,
                drone.target_hub,
                network
            )
            solution[drone] = path
            self.reservation_table.reserve_path(path)

        return solution

# tick()
# move drones
# update occupancy
# release reservations

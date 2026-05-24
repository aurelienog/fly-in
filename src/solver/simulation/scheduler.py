from dataclasses import dataclass

from ...domain import Drone, Network, Hub
from ..planners.base_multi_planner import BaseMultiPlanner
from ..planners.base_planner import BasePlanner
from ..planners.cbs import CBSPlanner
from .reservation_table import ReservationTable


@dataclass
class Scheduler:

    planner: BasePlanner | BaseMultiPlanner

    reservation_table: ReservationTable

    def schedule(
        self,
        drones: list[Drone],
        network: Network
    ) -> dict[Drone, list[Hub]]:

      if isinstance(
          self.planner,
          BaseMultiPlanner
      ):

          return self.planner.plan(
              drones,
              network
          )

      solution: dict[
            Drone,
            list[Hub]
        ]  = {}

      for drone in drones:

          solution[drone] = (
              self.planner.plan(
                  drone.start,
                  drone.goal,
                  network
              )
          )

      return solution

  # tick()

  # move drones

  # update occupancy

  # release reservations
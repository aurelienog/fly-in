from dataclasses import dataclass

from ..domain import Drone, Network
from .reservation_table import ReservationTable
from .models import SpaceTimeState
from .planner import SpaceTimeAStarPlanner


@dataclass
class Scheduler:
    """Coordinates multi-agent path planning and temporal reservation.

    The scheduler assigns conflict-free paths to multiple drones using a
    space-time planner and a shared reservation table.

    It ensures that each newly planned path is validated against already
    reserved resources, preventing collisions in both nodes and edges.
    """

    planner: SpaceTimeAStarPlanner

    reservation_table: ReservationTable

    def schedule(
        self,
        drones: list[Drone],
        network: Network
    ) -> dict[Drone,  list[SpaceTimeState]]:
        """Compute and assign space-time paths for a set of drones.

        Each drone is planned sequentially. After a path is computed, it
        is immediately reserved in the shared reservation table to ensure
        subsequent drones avoid conflicts.

        Args:
            drones: List of drones to schedule.
            network: Network in which drones operate.

        Returns:
            A mapping from each drone to its computed space-time path.
            Each path is a list of space-time states representing the
            drone's movement over time.
        """

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

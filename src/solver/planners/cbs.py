import heapq

from .base_multi_planner import BaseMultiPlanner
from .astar_space_time import SpaceTimeAStarPlanner

from ..models.cbs_node import CBSNode
from ..models.cbs_constraint import CBSConstraint
from ..models.cbs_conflict import CBSConflict

from ...domain import Drone, Network


class CBSPlanner(BaseMultiPlanner):

    def plan(
        self,
        drones: list[Drone],
        network: Network
    ) -> dict[Drone, list]:

        root_solution = {}

        # initial independent planning

        for drone in drones:

            planner = SpaceTimeAStarPlanner()

            path = planner.plan(
                drone.start,
                drone.goal,
                network
            )

            if not path:
                return {}

            root_solution[drone] = path

        root_cost = self.compute_cost(
            root_solution
        )

        root = CBSNode(
            cost=root_cost,
            constraints=set(),
            solution=root_solution
        )

        open_set = []

        heapq.heappush(
            open_set,
            root
        )

        while open_set:

            node = heapq.heappop(
                open_set
            )

            conflict = self.find_conflict(
                node.solution
            )

            if conflict is None:

                return node.solution

            for drone in (
                conflict.drone1,
                conflict.drone2
            ):

                new_constraints = set(
                    node.constraints
                )

                new_constraints.add(

                    CBSConstraint(
                        drone=drone,
                        hub=conflict.hub,
                        connection=conflict.connection,
                        timestep=conflict.timestep
                    )

                )

                new_solution = dict(
                    node.solution
                )

                planner = (
                    SpaceTimeAStarPlanner(
                        constraints=new_constraints
                    )
                )

                new_path = planner.plan(
                    drone.start,
                    drone.goal,
                    network
                )

                if not new_path:
                    continue

                new_solution[
                    drone
                ] = new_path

                new_cost = (
                    self.compute_cost(
                        new_solution
                    )
                )

                child = CBSNode(
                    cost=new_cost,
                    constraints=new_constraints,
                    solution=new_solution
                )

                heapq.heappush(
                    open_set,
                    child
                )

        return {}

    def compute_cost(
        self,
        solution
    ) -> float:

        return sum(
            len(path)
            for path
            in solution.values()
        )

    def find_conflict(
        self,
        solution
    ) -> CBSConflict | None:

        max_time = max(
            len(path)
            for path
            in solution.values()
        )

        for timestep in range(max_time):

            occupied = {}

            for drone, path in solution.items():

                if timestep >= len(path):

                    hub = path[-1]

                else:

                    hub = path[timestep]

                if hub in occupied:

                    other = occupied[hub]

                    return CBSConflict(

                        drone1=other,
                        drone2=drone,

                        timestep=timestep,

                        hub=hub
                    )

                occupied[hub] = drone

        return None



    # Multi-agent coordinator.

    # Usa A* internamente.

    # Flow:

    # CBS
    # ├── Drone1 → A*
    # ├── Drone2 → A*
    # ├── Drone3 → A*
    #         ↓
    # detect conflict
    #         ↓
    # add constraint
    #         ↓
    # replan
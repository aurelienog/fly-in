import heapq

from .base_planner import BasePlanner
from .astar_space_time import SpaceTimeAStarPlanner

from ..models.cbs_node import CBSNode

class CBSPlanner(BasePlanner):

    def __init__(self):

        self.low_level = (
            SpaceTimeAStarPlanner()
        )
    
    def find_conflict(
    self,
    solution: dict[Drone, list[Hub]]):


    def reconstruct_path(...):

        ...


Multi-agent coordinator.

Usa A* internamente.

Flow:

CBS
 ├── Drone1 → A*
 ├── Drone2 → A*
 ├── Drone3 → A*
        ↓
detect conflict
        ↓
add constraint
        ↓
replan
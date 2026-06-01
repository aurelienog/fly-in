from ..domain import Drone
from ..solver import SpaceTimeState


def render_drone_timeline(solution: dict[Drone, list[SpaceTimeState]]) -> None:
    for drone, path in solution.items():
        for state in path:
            print(f"{drone.id}-{state.hub.name} {state.timestep}")

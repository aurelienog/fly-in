from ..domain import Drone
from ..solver import SpaceTimeState

from collections import defaultdict


def render_drone_timeline(
    solution: dict[Drone, list[SpaceTimeState]]
) -> None:
    turns: dict[int, list[str]] = defaultdict(list)

    for drone, path in solution.items():
        for state in path[1:]:
            turns[state.timestep].append(
                f"{drone.id}-{state.hub.name}"
            )

    for timestep in sorted(turns):
        print(" ".join(turns[timestep]))

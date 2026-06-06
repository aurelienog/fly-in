from ..domain import Drone, Color, Hub
from .colors import RenderColors
from .state import HubState, ConnectionState, State

from collections import defaultdict


def render_terminal(
        solution: dict[Drone, list[State]]) -> None:

    turns: dict[int, list[str]] = defaultdict(list)
    previous_label: dict[Drone, str] = {}

    for drone, timeline in solution.items():
        timeline = sorted(timeline, key=lambda s: s.timestep)

        for state in timeline:

            #
            # HUB STATE
            #
            if isinstance(state, HubState):

                hub: Hub = state.hub

                if not getattr(hub, "color", None):
                    label = hub.name
                else:
                    color = hub.color

                    if color == Color.RAINBOW:
                        label = RenderColors.ANSI_rainbow(hub.name)
                    else:
                        label = (
                            f"{RenderColors.ANSI[color]}"
                            f"{hub.name}"
                            f"{RenderColors.ANSI[Color.DEFAULT]}"
                        )
            #
            # CONNECTION STATE
            #
            elif isinstance(state, ConnectionState):

                label = f"{state.from_hub.name}->{state.to_hub.name}"

            else:
                continue

            if previous_label.get(drone) != label:
                turns[state.timestep].append(f"{drone.id}-{label}")

            previous_label[drone] = label
    #
    # PRINT
    #
    for timestep in sorted(turns):
        if timestep == 0:
            continue
        # print(" ".join(turns[timestep]))
        print(f"T{timestep:03d}: " + " ".join(turns[timestep]))

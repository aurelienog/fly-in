from ..domain import Drone
from . import ColorPalette, HubState, ConnectionState, State

from collections import defaultdict


def render_drone_timeline(
        solution: dict[Drone, list[State]]) -> None:

    turns: dict[int, list[str]] = defaultdict(list)

    for drone, timeline in solution.items():

        for state in timeline:

            #
            # HUB STATE
            #
            if isinstance(state, HubState):

                hub = state.hub

                if not getattr(hub, "color", None):
                    label = hub.name
                else:
                    color = hub.color.upper()

                    if color == "RAINBOW":
                        label = ColorPalette.rainbow(hub.name)
                    else:
                        label = (
                            f"{getattr(ColorPalette, color)}"
                            f"{hub.name}"
                            f"{ColorPalette.RESET}"
                        )

                turns[state.timestep].append(
                    f"{drone.id}-{label}"
                )

            #
            # CONNECTION STATE
            #
            elif isinstance(state, ConnectionState):

                label = f"{state.from_hub.name}->{state.to_hub.name}"

                turns[state.timestep].append(
                    f"{drone.id}-{label}"
                )

    #
    # PRINT
    #
    for timestep in sorted(turns):
        print(f"T{timestep:03d}: " + " ".join(turns[timestep]))

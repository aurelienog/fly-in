from ..domain import Drone
from ..visualization import ColorPalette, HubState, ConnectionState, State

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
# def render_drone_timeline(
#     solution: dict[Drone, list[SpaceTimeState]]
# ) -> None:
#     turns: dict[int, list[str]] = defaultdict(list)

#     for drone, path in solution.items():
#         for state in path[1:]:
#             if not state.hub.color:
#                 colored_name = state.hub
#             else:
#                 color = state.hub.color.upper()
#                 if color == "RAINBOW":
#                     colored_name = ColorPalette.rainbow(state.hub.name)
#                 else:
#                     colored_name = f"{getattr(ColorPalette, color)}{state.hub.name}"
#                     f"{ColorPalette.RESET}"

#             turns[state.timestep].append(f"{drone.id}-{colored_name}")

#     for timestep in sorted(turns):
#         print(" ".join(turns[timestep]))

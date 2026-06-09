from ..domain import Drone, Color, Hub
from .colors import RenderColors
from .state import HubState, ConnectionState, State

from collections import defaultdict


def render_terminal(
        solution: dict[Drone, list[State]]) -> None:
    """Render a space-time simulation solution in the terminal.

    The function visualizes drone movements over time by grouping state
    transitions into timesteps and displaying occupancy information for
    hubs and connections. It also applies ANSI coloring for improved
    readability in terminal output.

    Args:
        solution: Mapping from each drone to its ordered list of
            space-time states representing its trajectory.

    Returns:
        None. The function prints a formatted timeline to stdout.
    """

    turns: dict[int, list[str]] = defaultdict(list)
    previous_location: dict[Drone, object] = {}

    hub_occupancy: defaultdict[int,
                               defaultdict[Hub, int]
                               ] = defaultdict(lambda: defaultdict(int))
    connection_occupancy: defaultdict[
                        int,
                        defaultdict[tuple[Hub, Hub], int]
                    ] = defaultdict(lambda: defaultdict(int))

    for drone, timeline in solution.items():
        timeline = sorted(timeline, key=lambda s: s.timestep)

        for state in timeline:

            if isinstance(state, HubState):
                location: tuple[str, Hub] | tuple[str, Hub, Hub] = ("hub", state.hub)

                hub_occupancy[state.timestep][state.hub] += 1
                hub: Hub = state.hub

                occupied = hub_occupancy[state.timestep][hub]

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
                            f"<{occupied}/{hub.max_drones}>"
                            f"{RenderColors.ANSI[Color.DEFAULT]}"
                        )
            #
            # CONNECTION STATE
            #
            elif isinstance(state, ConnectionState):
                location = (
                    "connection",
                    state.from_hub,
                    state.to_hub
                )
                key = (state.from_hub, state.to_hub)

                connection_occupancy[state.timestep][key] += 1
                occupied = connection_occupancy[state.timestep][(
                    state.from_hub, state.to_hub)]

                label = (f"{state.from_hub.name}->{state.to_hub.name}"
                         f"<{occupied}/{state.connection.max_link_capacity}>")
            else:
                continue

            if previous_location.get(drone) != location:
                turns[state.timestep].append(f"{drone.id}-{label}")

            previous_location[drone] = location
    #
    # PRINT
    #
    for timestep in sorted(turns):
        if timestep == 0:
            continue
        # print(" ".join(turns[timestep]))
        print(f"T{timestep:03d}: " + " ".join(turns[timestep]))

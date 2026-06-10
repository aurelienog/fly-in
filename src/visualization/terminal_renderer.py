from .state import State, HubState, ConnectionState
from ..domain import Drone, Hub, Color
from .colors import RenderColors

from collections import defaultdict


class TerminalRenderer():
    """Render simulation timelines in the terminal."""
    def __init__(self) -> None:
        """Initialize the renderer."""
        self.has_colors = False

    def render_compact(self, simulation: dict[Drone, list[State]]) -> None:
        """Render a compact simulation timeline.

        Displays only drone location changes. Each output line represents
        a simulation timestep.

        Args:
            simulation: Mapping of drones to their ordered state timelines.
        """
        turns = self._build_turns(simulation, detailed=False)
        self._print_turns(turns, detailed=False)

    def render_detailed(self, simulation: dict[Drone, list[State]]) -> None:
        """Render a detailed simulation timeline.

        Displays drone location changes together with occupancy information
        for hubs and connections.

        Args:
            simulation: Mapping of drones to their ordered state timelines.
        """
        turns = self._build_turns(simulation, detailed=True)
        self._print_turns(turns, detailed=True)

    def _build_turns(
        self,
        simulation: dict[Drone, list[State]],
        detailed: bool,
    ) -> dict[int, list[str]]:
        """Build a timestep-indexed representation of the simulation.

        Converts drone timelines into a structure suitable for terminal
        rendering by grouping state transitions by timestep.

        Args:
            simulation: Mapping of drones to their ordered state timelines.
            detailed: Whether occupancy information should be included.

        Returns:
            A mapping from timestep to rendered state transition strings.
        """
        turns: dict[int, list[str]] = defaultdict(list)
        previous_location: dict[Drone, object] = {}

        hub_occupancy: defaultdict[
            int,
            defaultdict[Hub, int]
            ] = defaultdict(lambda: defaultdict(int))

        connection_occupancy: defaultdict[
            int,
            defaultdict[tuple[Hub, Hub], int]
            ] = defaultdict(lambda: defaultdict(int))

        for drone, timeline in simulation.items():
            timeline = sorted(timeline, key=lambda s: s.timestep)

            for state in timeline:

                location, label = self._state_label(
                    state,
                    detailed,
                    hub_occupancy,
                    connection_occupancy,
                )

                if location is None:
                    continue

                if previous_location.get(drone) != location:
                    turns[state.timestep].append(f"{drone.id}-{label}")

                previous_location[drone] = location

        return turns

    def _state_label(
        self,
        state: State,
        detailed: bool,
        hub_occupancy: defaultdict[int, defaultdict[Hub, int]],
        connection_occupancy: defaultdict[int, defaultdict[tuple[Hub, Hub], int]]
    ) -> tuple[tuple[str, Hub] | tuple[str, Hub, Hub], str] | tuple[None, str]:
        """Generate a location identifier and label for a state.

        Args:
            state: State to render.
            detailed: Whether occupancy information should be included.
            hub_occupancy: Hub occupancy counters indexed by timestep.
            connection_occupancy: Connection occupancy counters indexed by
                timestep.

        Returns:
            A tuple containing the state location identifier and its
            rendered label. Returns ``(None, "")`` for unsupported states.
        """

        location: tuple[str, Hub] | tuple[str, Hub, Hub]

        if isinstance(state, HubState):
            hub_occupancy[state.timestep][state.hub] += 1
            hub = state.hub

            location = ("hub", hub)
            occupied = hub_occupancy[state.timestep][hub]
            return (location, self._hub_label(hub, occupied, detailed))

        elif isinstance(state, ConnectionState):
            key = (state.from_hub, state.to_hub)
            connection_occupancy[state.timestep][key] += 1

            location = (
                    "connection",
                    state.from_hub,
                    state.to_hub
                )

            occupied = connection_occupancy[state.timestep][(
                state.from_hub, state.to_hub)]

            return (location, self._connection_label(state,  occupied, detailed))

        else:
            return (None, "")

    def _hub_label(
        self,
        hub: Hub,
        occupied: int,
        detailed: bool
    ) -> str:
        """Build the terminal label for a hub state.

        Args:
            hub: Hub being rendered.
            occupied: Number of drones occupying the hub at the timestep.
            detailed: Whether occupancy information should be included.

        Returns:
            The formatted hub label.
        """
        label = []

        if self.has_colors:
            color = hub.color
            if color == Color.RAINBOW:
                label.append(RenderColors.ANSI_rainbow(hub.name))
            else:
                label.append(f"{RenderColors.ANSI[color]}{hub.name}")
        else:
            label.append(f"{hub.name}")

        if detailed:
            label.append(f"<{occupied}/{hub.max_drones}>")

        if self.has_colors:
            label.append(f"{RenderColors.ANSI[Color.DEFAULT]}")

        return "".join(label)

    def _connection_label(
        self,
        state: ConnectionState,
        occupied: int,
        detailed: bool
    ) -> str:
        """Build the terminal label for a connection state.

        Args:
            state: Connection state being rendered.
            occupied: Number of drones using the connection at the timestep.
            detailed: Whether occupancy information should be included.

        Returns:
            The formatted connection label.
        """
        label: list[str] = []

        label.append(f"{state.from_hub.name}->{state.to_hub.name}")
        if detailed:
            label.append(f"<{occupied}/{state.connection.max_link_capacity}>")

        return "".join(label)

    def _print_turns(
            self,
            turns: dict[int, list[str]],
            detailed: bool) -> None:
        """Print a rendered simulation timeline.

        Args:
            turns: Mapping of timesteps to rendered entries.
            detailed: Whether to include timestep prefixes.
        """
        for timestep in sorted(turns):
            if timestep == 0:
                continue

            line = " ".join(turns[timestep])

            if detailed:
                print(f"T{timestep:03d}: {line}")
            else:
                print(line)

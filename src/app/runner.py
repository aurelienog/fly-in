from .file_loader import load_simulation
from ..solver import SpaceTimeAStarPlanner, ReservationTable, Scheduler
from ..visualization import TimelineExpander, TerminalRenderer, Game


def run_app(filename: str, render_mode: str | None) -> None:
    """Run the drone simulation application from a simulation file.

    Args:
        filename: Path to the file containing the simulation definition.

    Returns:
        None. This function executes the complete simulation workflow,
        including loading, planning, scheduling, visualization, and
        terminal rendering.
    """
    render_options = {"pygame", "visual"}

    if render_mode and render_mode not in render_options:
        raise ValueError(
            f"Invalid render mode: {render_mode!r}.\n"
            f"Available render modes: {', '.join(sorted(render_options))}.\n"
            f"Default: compact rendering (no value)."
        )

    network, drones = load_simulation(filename)

    reservation_table = ReservationTable()
    planner = SpaceTimeAStarPlanner(reservation_table)
    scheduler = Scheduler(planner, reservation_table)
    solution = scheduler.schedule(drones, network)

    expander = TimelineExpander()
    simulation = {
        drone: expander.expand(path)
        for drone, path in solution.items()
    }

    terminal_renderer = TerminalRenderer()

    if render_mode == "visual":
        terminal_renderer.has_colors = True
        terminal_renderer.render_detailed(simulation)

    elif render_mode == "pygame":
        Game(network, simulation).run()
    else:
        terminal_renderer.render_compact(simulation)

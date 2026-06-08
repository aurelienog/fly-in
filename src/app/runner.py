from .file_loader import load_simulation
from ..solver import SpaceTimeAStarPlanner, ReservationTable, Scheduler
from ..visualization import TimelineExpander, render_terminal, Game


def run_app(filename: str) -> None:
    """Run the drone simulation application from a simulation file.

    Args:
        filename: Path to the file containing the simulation definition.

    Returns:
        None. This function executes the complete simulation workflow,
        including loading, planning, scheduling, visualization, and
        terminal rendering.
    """
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
    game = Game(network, simulation)
    game.run()
    render_terminal(simulation)

from ..io import load_simulation, render_drone_timeline
from ..solver import SpaceTimeAStarPlanner, ReservationTable, Scheduler
from ..visualization import TimelineExpander


def run_app(filename: str) -> None:

    network, drones = load_simulation(filename)

    reservation_table = ReservationTable()
    planner = SpaceTimeAStarPlanner(reservation_table)
    scheduler = Scheduler(planner, reservation_table)
    solution = scheduler.schedule(drones, network)

    expander = TimelineExpander()
    timeline_solution = {
        drone: expander.expand(path)
        for drone, path in solution.items()
    }

    render_drone_timeline(timeline_solution)

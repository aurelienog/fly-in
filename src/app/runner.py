from ..io import load_simulation, render_drone_timeline
from ..solver import Scheduler, CBSPlanner, SpaceTimeAStarPlanner, ReservationTable


def run_app(filename: str) -> None:

    network, drones = load_simulation(filename)

    reservation_table = ReservationTable()
    planner = SpaceTimeAStarPlanner(reservation_table)
    scheduler = Scheduler(planner, reservation_table)

    solution = scheduler.schedule(drones, network)
    render_drone_timeline(solution)
    print("ok")

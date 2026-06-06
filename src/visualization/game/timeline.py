from collections import defaultdict
from ...domain import Drone
from ...solver import SpaceTimeState


class Timeline:
    """Organiza los estados de cada drone por timestep para fácil acceso."""

    def __init__(self, solution: dict[Drone, list[SpaceTimeState]]):
        """
        Args:
            solution: diccionario {drone: lista de SpaceTimeState}
        """
        self._timeline = defaultdict(dict)  # {timestep: {drone: SpaceTimeState}}
        self.solution = solution
        self.max_timestep = 0

        for drone, states in solution.items():
            for state in states:
                self._timeline[state.timestep][drone] = state
                self.max_timestep = max(self.max_timestep, state.timestep)

    def states_at(self, timestep: int) -> dict[Drone, SpaceTimeState]:
        """Retorna todos los estados (de todos los drones) en un timestep específico."""
        if timestep in self._timeline:
            return self._timeline[timestep]
        return {}

    def get_all_timesteps(self) -> list[int]:
        """Retorna lista de todos los timesteps disponibles."""
        return sorted(self._timeline.keys())

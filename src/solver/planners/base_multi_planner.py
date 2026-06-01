from abc import ABC, abstractmethod

from ...domain import Drone, Network
from ..models import SpaceTimeState


class BaseMultiPlanner(ABC):

    @abstractmethod
    def plan(
        self,
        drones: list[Drone],
        network: Network
    ) -> dict[Drone, list[SpaceTimeState]]:
        pass

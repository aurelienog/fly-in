from abc import ABC, abstractmethod

from ...domain import Drone, Network


class BaseMultiPlanner(ABC):

    @abstractmethod
    def plan(
        self,
        drones: list[Drone],
        network: Network
    ) -> dict[Drone, list]:
        pass

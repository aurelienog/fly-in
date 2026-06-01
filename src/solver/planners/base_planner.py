from abc import ABC, abstractmethod

from ...domain import Network, Hub
from ..models import SpaceTimeState


class BasePlanner(ABC):

    @abstractmethod
    def plan(
        self,
        drone,
        start: Hub,
        goal: Hub,
        network: Network
    ) -> list[SpaceTimeState]:
        pass

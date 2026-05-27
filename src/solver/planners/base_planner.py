from abc import ABC, abstractmethod

from ...domain import Network, Hub


class BasePlanner(ABC):

    @abstractmethod
    def plan(
        self,
        start: Hub,
        goal: Hub,
        network: Network
    ) -> list:
        pass

from abc import ABC, abstractmethod
from typing import TypeVar

from ...domain import Network, Hub

Node = TypeVar("Node")


class BasePlanner(ABC):

    @abstractmethod
    def plan(
        self,
        start: Hub,
        goal: Hub,
        network: Network
    ) -> list[Hub] | list[tuple[Hub, int]] :
        pass

    def reconstruct_path(
            self,
            came_from: dict[Node, Node | None],
            current: Node
        ) -> list[Node]:
        """
        Default path reconstruction.
        """

        path = []

        while current is not None:

            path.append(current)

            current = came_from.get(current)

        path.reverse()

        return path

from dataclasses import dataclass, field
from itertools import count

from .cbs_constraint import CBSConstraint
from ...domain import Drone


@dataclass(order=True)
class CBSNode:

    cost: float = field(compare=True)

    constraints: set[CBSConstraint] = field(compare=False)

    solution: dict[Drone, list] = field(compare=False)

    node_id: int = field(default_factory=count().__next__, compare=True)

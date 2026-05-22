from dataclasses import dataclass

from .cbs_constraint import CBSConstraint
from ...domain import Drone, Hub


@dataclass
class CBSNode:

    constraints: set[CBSConstraint]

    solution: dict[
        Drone,
        list[Hub]
    ]

    cost: float
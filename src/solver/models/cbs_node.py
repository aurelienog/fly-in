from dataclasses import dataclass, field

from .cbs_constraint import CBSConstraint
from ...domain import Drone, Hub


@dataclass(order=True)
class CBSNode:

    cost: float

    constraints: set[CBSConstraint] = field(
        compare=False
    )

    solution: dict[
        Drone,
        list[Hub]
    ] = field(
        compare=False
    )

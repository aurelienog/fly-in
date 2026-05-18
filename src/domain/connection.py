from __future__ import annotations

from typing import TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    from .hub import Hub


@dataclass
class Connection:
    hubs: tuple[Hub, Hub]
    max_link_capacity: int = 1
    occupation: int = 0

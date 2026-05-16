from dataclasses import dataclass
from . import Hub


@dataclass
class Connection:
    hubs: tuple[Hub, Hub]
    max_link_capacity: int = 1
    occupation: int = 0

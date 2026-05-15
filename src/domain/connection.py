from dataclasses import dataclass
from . import Hub


@dataclass
class Connection:
    max_link_capacity: int
    occupation: int
    hubs: tuple[Hub, Hub]

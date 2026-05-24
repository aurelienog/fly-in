from .hub import Hub
from dataclasses import dataclass


@dataclass
class Drone:
    id: int
    current_hub: Hub
    target_hub: Hub

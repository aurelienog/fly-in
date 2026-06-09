from .hub import Hub
from dataclasses import dataclass


@dataclass
class Drone:
    id: str
    current_hub: Hub
    target_hub: Hub

    def __hash__(self) -> int:
        return hash(self.id)

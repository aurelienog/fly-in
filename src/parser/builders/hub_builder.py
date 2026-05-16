from ..models import RawHub
from ...domain import Hub


def build_hub(raw_hub: RawHub) -> Hub:
    return Hub(
        name=raw_hub.name,
        x=raw_hub.x,
        y=raw_hub.y,
        zone=raw_hub.zone,
        color=raw_hub.color,
        max_drones=raw_hub.max_drones,
    )

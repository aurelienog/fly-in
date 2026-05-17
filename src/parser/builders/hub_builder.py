from ..models import RawHub
from ...domain import Hub, HubRole, ZoneType


def build_hub(raw: RawHub) -> Hub:
    return Hub(
        name=raw.name,

        position=(
            raw.x,
            raw.y,
        ),
        role=HubRole(raw.hub_type),

        zone=ZoneType(raw.zone),

        max_drones=raw.max_drones,

        color=raw.color or "default"
    )

from ..models import RawHub
from ...domain import Hub, HubRole, ZoneType


def build_hub(raw: RawHub) -> Hub:
    if raw.hub_type == HubRole.START:
        hub_role = HubRole.START
    elif raw.hub_type == HubRole.END:
        hub_role = HubRole.END
    else:
        hub_role = HubRole.HUB

    return Hub(
        name=raw.name,

        position=(
            raw.x,
            raw.y,
        ),
        role=hub_role,

        zone=ZoneType(raw.zone),

        max_drones=raw.max_drones,

        color=raw.color
    )

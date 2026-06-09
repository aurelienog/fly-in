from ..models import RawHub
from ...domain import Hub, HubRole, ZoneType, Color


def build_hub(raw: RawHub) -> Hub:
    """Create a hub from its raw representation.

    Args:
        raw: Raw hub data containing the hub properties and
            configuration.

    Returns:
        The constructed hub instance.
    """
    if raw.hub_type == HubRole.START.value:
        hub_role = HubRole.START
    elif raw.hub_type == HubRole.END.value:
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

        color=Color(raw.color)
    )

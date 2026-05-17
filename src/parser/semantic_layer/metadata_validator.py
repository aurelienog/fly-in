from ...errors import SemanticError
from .. import RawHub, RawConnection
from ...domain import ZoneType, HubRole


def validate_hub_metadata(raw_hub: RawHub) -> None:
    try:
        ZoneType(raw_hub.zone)
        HubRole(raw_hub.hub_type)

    except ValueError as error:
        raise SemanticError(error)

    if raw_hub.max_drones <= 0:
        raise SemanticError(
            "max_drones must be positive"
        )


def validate_connection_metadata(
    raw_connection: RawConnection,
) -> None:

    if raw_connection.max_link_capacity <= 0:
        raise SemanticError(...)

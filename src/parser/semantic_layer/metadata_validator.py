from ...errors import SemanticError
from ..models import RawHub, RawConnection
from ...domain import ZoneType
from ...domain import Color


def validate_hub_metadata(raw_hub: RawHub) -> None:
    try:
        ZoneType(raw_hub.zone)

    except ValueError as exc:
        raise SemanticError(f"line {raw_hub.line} invalid zone type: {raw_hub.zone}"
                            ) from exc
    try:
        Color(raw_hub.color)

    except ValueError as exc:
        raise SemanticError(f"line {raw_hub.line} invalid color: {raw_hub.color}"
                            ) from exc

    if raw_hub.max_drones <= 0:
        raise SemanticError(f"line {raw_hub.line} max_drones must be positive")


def validate_connection_metadata(
    raw_connection: RawConnection,
) -> None:

    if raw_connection.max_link_capacity <= 0:
        raise SemanticError(
            f"line {raw_connection.line}: max_link_capacity must be a positiv integer"
        )

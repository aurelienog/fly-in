from ...errors import SemanticError
from ..models import RawHub, RawConnection
from ...domain import ZoneType
from ...domain import Color


def validate_hub_metadata(raw_hub: RawHub) -> None:
    """Validate the metadata associated with a raw hub definition.

    The validation checks that the zone type and color are supported and
    that the maximum drone capacity is positive.

    Args:
        raw_hub: Raw hub data to validate.

    Returns:
        None.

    Raises:
        SemanticError: If the zone type is invalid, the color is
            unsupported, or the maximum drone capacity is not positive.
    """
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
    """Validate the metadata associated with a raw connection definition.

    Args:
        raw_connection: Raw connection data to validate.

    Returns:
        None.

    Raises:
        SemanticError: If the maximum link capacity is not positive.
    """

    if raw_connection.max_link_capacity <= 0:
        raise SemanticError(
            f"line {raw_connection.line}: max_link_capacity must be a positiv integer"
        )

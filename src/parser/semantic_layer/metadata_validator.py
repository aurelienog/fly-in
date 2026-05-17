from ...errors import SemanticError
from .. import RawHub, RawConnection


def validate_hub_metadata(raw_hub: RawHub) -> None:
    VALID_ZONES = {
      "normal",
      "blocked",
      "restricted",
      "priority",
    }

    if raw_hub.zone not in VALID_ZONES:
        raise SemanticError(
            f"invalid zone type: {raw_hub.zone}"
        )

    if raw_hub.max_drones <= 0:
        raise SemanticError(
            "max_drones must be positive"
        )


def validate_connection_metadata(
    raw_connection: RawConnection,
) -> None:

    if raw_connection.max_link_capacity <= 0:
        raise SemanticError(...)

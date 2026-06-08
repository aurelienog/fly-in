from ..models import RawNetwork, RawHub
from ...errors import SemanticError
from ...domain import HubRole
from .metadata_validator import (validate_hub_metadata,
                                 validate_connection_metadata)


def validate_unique_hubs(
    hubs: list[RawHub],
) -> None:
    """Validate that all hub names are unique.

    Args:
        hubs: Hub definitions to validate.

    Raises:
        SemanticError: If two or more hubs share the same name.
    """

    seen: set[str] = set()

    for hub in hubs:

        if hub.name in seen:
            raise SemanticError(f"line {hub.line}: Hub names must be unique")

        seen.add(hub.name)


def validate_start_end(
    hubs: list[RawHub],
) -> None:
    """Validate the presence of exactly one start hub and one end hub.

    The function also verifies that every hub role is valid.

    Args:
        hubs: Hub definitions to validate.

    Raises:
        SemanticError: If a hub role is invalid, if no start or end hub
            is defined, or if multiple start or end hubs are defined.
    """

    start_count = 0
    end_count = 0

    start_lines = []
    end_lines = []

    for hub in hubs:
        try:
            role = HubRole(hub.hub_type)
        except ValueError as exc:
            raise SemanticError(
                f"line {hub.line}: invalid hub role: {hub.hub_type}"
            ) from exc

        if role is HubRole.START:
            start_count += 1
            start_lines.append(hub.line)

        elif role is HubRole.END:
            end_count += 1
            end_lines.append(hub.line)

    if start_count != 1:
        raise SemanticError(
            f"found {start_count} start_hub(s), expected exactly one"
            )

    if end_count != 1:
        raise SemanticError(
            f"found {end_count} end_hub(s), expected exactly one"
            )


def validate_connections(
    raw: RawNetwork,
) -> None:
    """Validate all connection definitions in a network.

    The validation ensures that connections reference existing hubs,
    do not create self-connections, and are not duplicated.

    Args:
        raw: Raw network data containing hub and connection
            definitions.

    Raises:
        SemanticError: If a connection references an unknown hub,
            creates a self-connection, or duplicates an existing
            connection.
    """

    existing_hubs = {hub.name for hub in raw.hubs}
    seen_connections: set[frozenset[str]] = set()

    for connection in raw.connections:
        if connection.a not in existing_hubs:
            raise SemanticError(
                f"line {connection.line}: Unknown hub in connection: {connection.a}"
            )

        if connection.b not in existing_hubs:
            raise SemanticError(
                f"line {connection.line}: Unknown hub in connection: {connection.b}"
            )

        if connection.a == connection.b:
            raise SemanticError(
                f"line {connection.line}: self-connections are not allowed"
            )

        key = frozenset({
            connection.a,
            connection.b,
        })

        if key in seen_connections:
            raise SemanticError(
                f"line {connection.line}: duplicate connection"
            )

        seen_connections.add(key)


def validate_unique_coordinates(
    hubs: list[RawHub],
) -> None:
    """Validate that all hubs have unique coordinates.

    Args:
        hubs: Hub definitions to validate.

    Raises:
        SemanticError: If two or more hubs share the same coordinates.
    """

    seen: dict[tuple[int, int], int] = {}

    for hub in hubs:
        coords = (hub.x, hub.y)

        if coords in seen:
            raise SemanticError(
                f"line {hub.line}: coordinates {coords} "
                f"already used on line {seen[coords]}"
            )

        seen[coords] = hub.line


def validate_network(raw: RawNetwork) -> None:
    """Validate the semantic correctness of a raw network definition.

    The validation includes drone count, hub definitions, hub
    coordinates, start and end hubs, connection definitions, and
    metadata consistency.

    Args:
        raw: Raw network data to validate.

    Raises:
        SemanticError: If any semantic validation rule is violated.
    """

    if raw.nb_drones <= 0:
        raise SemanticError("First line error: Drone count must be positive")

    validate_unique_hubs(raw.hubs)
    validate_unique_coordinates(raw.hubs)
    validate_start_end(raw.hubs)
    validate_connections(raw)

    for raw_hub in raw.hubs:
        validate_hub_metadata(raw_hub)

    for raw_connection in raw.connections:
        validate_connection_metadata(raw_connection)

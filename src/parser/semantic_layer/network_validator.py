from ..models import RawNetwork, RawHub
from ...errors import SemanticError
from ...domain import HubRole
from .metadata_validator import (validate_hub_metadata, 
                                 validate_connection_metadata)


def validate_hub_role(raw_hub: RawHub) -> None:

    try:
        HubRole(raw_hub.hub_type)

    except ValueError as exc:
        raise SemanticError(f"invalid hub role: {raw_hub.hub_type}") from exc


def validate_unique_hubs(
    hubs: list[RawHub],
) -> None:

    seen: set[str] = set()

    for hub in hubs:

        if hub.name in seen:
            raise SemanticError("Hub names must be unique")

        seen.add(hub.name)


def validate_start_end(
    hubs: list[RawHub],
) -> None:

    start_count = 0
    end_count = 0

    for hub in hubs:
        role = HubRole(hub.hub_type)

        if role is HubRole.START:
            start_count += 1

        elif role is HubRole.END:
            end_count += 1

    if start_count != 1:
        raise SemanticError("Network must contain exactly one start_hub")

    if end_count != 1:
        raise SemanticError("Network must contain exactly one end_hub")


def validate_connections(
    raw: RawNetwork,
) -> None:

    existing_hubs = {hub.name for hub in raw.hubs}
    seen_connections: set[frozenset[str]] = set()

    for connection in raw.connections:
        if connection.a not in existing_hubs:
            raise SemanticError(
                f"Unknown hub in connection: {connection.a}"
            )

        if connection.b not in existing_hubs:
            raise SemanticError(
                f"Unknown hub in connection: {connection.b}"
            )

        key = frozenset({
            connection.a,
            connection.b,
        })

        if key in seen_connections:
            raise SemanticError(
                "duplicate connection"
            )

        seen_connections.add(key)


def validate_network(raw: RawNetwork) -> None:

    if raw.nb_drones <= 0:
        raise SemanticError("Drone count must be positive")

    validate_unique_hubs(raw.hubs)
    validate_start_end(raw.hubs)
    validate_connections(raw)

    for raw_hub in raw.hubs:
        validate_hub_metadata(raw_hub)

    for raw_connection in raw.connections:
        validate_connection_metadata(raw_connection)


# Semántica es cuando preguntas:

# ¿Existe exactamente un start_hub?
# ¿Existe exactamente un end_hub?
# ¿Los nombres son únicos?
# ¿Un connection referencia hubs existentes?
# ¿nb_drones > 0?
# ¿zone=blocked se usa correctamente?
# ¿capacidades son coherentes?


# validación + enums + rules

# | Etapa      | Responsabilidad          |
# | ---------- | ------------------------ |
# | Parsing    | Sintaxis                 |
# | Validation | Reglas semánticas        |
# | Build      | Transformar Raw → Domain |

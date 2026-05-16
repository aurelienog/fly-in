from .. import RawNetwork, RawHub
from ...errors import SemanticError


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

        if hub.hub_type == "start_hub":
            start_count += 1

        elif hub.hub_type == "end_hub":
            end_count += 1

    if start_count != 1:
        raise SemanticError("Network must contain exactly one start_hub")

    if end_count != 1:
        raise SemanticError("Network must contain exactly one end_hub")


def validate_connections(
    raw: RawNetwork,
) -> None:

    for connection in raw.connections:
        if connection.a not in existing_hubs:
            raise SemanticError(
                f"Unknown hub in connection: {connection.a}"
            )

        if connection.b not in existing_hubs:
            raise SemanticError(
                f"Unknown hub in connection: {connection.b}"
            )


def validate_network(raw: RawNetwork) -> None:

    if raw.nb_drones <= 0:
        raise SemanticError("Drone count must be positive")

    validate_unique_hubs(raw.hubs)
    validate_start_end(raw.hubs)
    validate_connections(raw)


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

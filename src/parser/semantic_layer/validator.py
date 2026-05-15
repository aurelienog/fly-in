from .. import RawNetwork
from ...errors import SemanticError


def validate_network(raw: RawNetwork) -> None:
    if raw.nb_drones <= 0:
        raise SemanticError("Drone count must be positive")

    start_hubs = [h for h in raw.hubs if h.hub_type == "start_hub"]
    end_hubs = [h for h in raw.hubs if h.hub_type == "end_hub"]

    if len(start_hubs) != 1:
        raise SemanticError("Network must contain exactly one start_hub")

    if len(end_hubs) != 1:
        raise SemanticError("Network must contain exactly one end_hub")

    names = [h.name for h in raw.hubs]

    if len(names) != len(set(names)):
        raise SemanticError("Hub names must be unique")

    existing_hubs = set(names)

    for connection in raw.connections:
        if connection.a not in existing_hubs:
            raise SemanticError(
                f"Unknown hub in connection: {connection.a}"
            )

        if connection.b not in existing_hubs:
            raise SemanticError(
                f"Unknown hub in connection: {connection.b}"
            )

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

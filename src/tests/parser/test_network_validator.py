from __future__ import annotations

import pytest

from ...errors import SemanticError

from ...parser.models import (
        RawHub,
        RawConnection,
        RawNetwork,
    )

from ...parser.semantic_layer.network_validator import (
    validate_hub_role,
    validate_unique_hubs,
    validate_start_end,
    validate_connections,
    validate_network,
)
from ...parser.semantic_layer.metadata_validator import (
    validate_hub_metadata,
    validate_connection_metadata,
)


# =========================================================
# validate_hub_role
# =========================================================


def test_validate_invalid_hub_role() -> None:
    raw_hub = RawHub(
        line=1,
        hub_type="invalid",
        name="roof1",
        x=1,
        y=1,
        zone="normal",
        color="green",
        max_drones=1,
    )

    with pytest.raises(SemanticError):
        validate_hub_role(raw_hub)


# =========================================================
# validate_unique_hubs
# =========================================================


def test_validate_duplicate_hubs() -> None:
    hubs = [
        RawHub(
            line=1,
            hub_type="hub",
            name="roof1",
            x=1,
            y=1,
            zone="normal",
            color="green",
            max_drones=1,
        ),
        RawHub(
            line=2,
            hub_type="hub",
            name="roof1",
            x=2,
            y=2,
            zone="priority",
            color="red",
            max_drones=2,
        ),
    ]

    with pytest.raises(SemanticError):
        validate_unique_hubs(hubs)


# =========================================================
# validate_start_end
# =========================================================


def test_validate_multiple_starts() -> None:
    hubs = [
        RawHub(
            line=1,
            hub_type="start_hub",
            name="start1",
            x=0,
            y=0,
            zone="normal",
            color="green",
            max_drones=1,
        ),
        RawHub(
            line=2,
            hub_type="start_hub",
            name="start2",
            x=1,
            y=1,
            zone="normal",
            color="green",
            max_drones=1,
        ),
    ]

    with pytest.raises(SemanticError):
        validate_start_end(hubs)


def test_validate_missing_end() -> None:
    hubs = [
        RawHub(
            line=1,
            hub_type="start_hub",
            name="start",
            x=0,
            y=0,
            zone="normal",
            color="green",
            max_drones=1,
        ),
    ]

    with pytest.raises(SemanticError):
        validate_start_end(hubs)


# =========================================================
# validate_connections
# =========================================================


def test_validate_connection_unknown_hub_a() -> None:
    raw = RawNetwork(
        nb_drones=1,
        hubs=[
            RawHub(
                line=1,
                hub_type="hub",
                name="roof1",
                x=1,
                y=1,
                zone="normal",
                color="green",
                max_drones=1,
            ),
        ],
        connections=[
            RawConnection(
                line=2,
                a="unknown",
                b="roof1",
                max_link_capacity=1,
            ),
        ],
    )

    with pytest.raises(SemanticError):
        validate_connections(raw)


def test_validate_connection_unknown_hub_b() -> None:
    raw = RawNetwork(
        nb_drones=1,
        hubs=[
            RawHub(
                line=1,
                hub_type="hub",
                name="roof1",
                x=1,
                y=1,
                zone="normal",
                color="green",
                max_drones=1,
            ),
        ],
        connections=[
            RawConnection(
                line=2,
                a="roof1",
                b="unknown",
                max_link_capacity=1,
            ),
        ],
    )

    with pytest.raises(SemanticError):
        validate_connections(raw)


def test_validate_duplicate_connection() -> None:
    raw = RawNetwork(
        nb_drones=1,
        hubs=[
            RawHub(
                line=1,
                hub_type="hub",
                name="roof1",
                x=1,
                y=1,
                zone="normal",
                color="green",
                max_drones=1,
            ),
            RawHub(
                line=2,
                hub_type="hub",
                name="roof2",
                x=2,
                y=2,
                zone="priority",
                color="red",
                max_drones=2,
            ),
        ],
        connections=[
            RawConnection(
                line=3,
                a="roof1",
                b="roof2",
                max_link_capacity=1,
            ),
            RawConnection(
                line=4,
                a="roof2",
                b="roof1",
                max_link_capacity=1,
            ),
        ],
    )

    with pytest.raises(SemanticError):
        validate_connections(raw)


# =========================================================
# validate_hub_metadata
# =========================================================


def test_validate_invalid_zone_type() -> None:
    raw_hub = RawHub(
        line=1,
        hub_type="hub",
        name="roof1",
        x=1,
        y=1,
        zone="invalid_zone",
        color="green",
        max_drones=1,
    )

    with pytest.raises(SemanticError):
        validate_hub_metadata(raw_hub)


def test_validate_negative_max_drones() -> None:
    raw_hub = RawHub(
        line=1,
        hub_type="hub",
        name="roof1",
        x=1,
        y=1,
        zone="normal",
        color="green",
        max_drones=-1,
    )

    with pytest.raises(SemanticError):
        validate_hub_metadata(raw_hub)


# =========================================================
# validate_connection_metadata
# =========================================================


def test_validate_negative_link_capacity() -> None:
    raw_connection = RawConnection(
        line=1,
        a="roof1",
        b="roof2",
        max_link_capacity=-1,
    )

    with pytest.raises(SemanticError):
        validate_connection_metadata(raw_connection)


# =========================================================
# validate_network
# =========================================================


def test_validate_network_invalid_drone_count() -> None:
    raw = RawNetwork(
        nb_drones=0,
        hubs=[],
        connections=[],
    )

    with pytest.raises(SemanticError):
        validate_network(raw)

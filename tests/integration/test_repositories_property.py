from datetime import datetime, timedelta

import pytest

from loguru import logger
from json import dumps
from home_budget.config import CONFIG
from home_budget.db import Database
from home_budget.models.property import Property, PropertyType
from home_budget.repositories.property import PropertyRepository


def test_insert_returns_property_db() -> None:
    creation_time = datetime(2026, 2, 8, 12, 0, 0)
    property_item = Property(
        creation_time=creation_time,
        name="Wallet",
        type=PropertyType.CASH,
        amount=1200.50,
    )

    inserted = PropertyRepository.insert(property_item)

    assert inserted.id_p > 0
    assert inserted.creation_time == creation_time
    assert inserted.name == "Wallet"
    assert inserted.type == PropertyType.CASH
    assert inserted.amount == 1200.50


def test_select_all() -> None:
    all_properties = PropertyRepository.select()

    json_output = dumps(
        [prop.model_dump() for prop in all_properties], default=str, indent=2
    )

    logger.info(f"All properties:\n{json_output}")

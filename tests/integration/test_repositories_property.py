import pytest

from loguru import logger
from json import dumps
from home_budget.config import CONFIG
from home_budget.db import Database
from home_budget.models.property import Property, PropertyType
from home_budget.repositories.property import PropertyRepository


def test_insert_returns_property_db() -> None:
    year_month_of_creation = "2026-02"
    property_item = Property(
        year_month_of_creation=year_month_of_creation,
        name="Wallet",
        type=PropertyType.CASH,
        amount=1200.50,
    )

    inserted = PropertyRepository.insert(property_item)

    assert inserted.id_p > 0
    assert inserted.year_month_of_creation == year_month_of_creation
    assert inserted.name == "Wallet"
    assert inserted.type == PropertyType.CASH
    assert inserted.amount == 1200.50


def test_select_all() -> None:
    all_properties = PropertyRepository.select()

    json_output = dumps(
        [prop.model_dump() for prop in all_properties], default=str, indent=2
    )

    logger.info(f"All properties:\n{json_output}")

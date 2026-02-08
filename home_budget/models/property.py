from pydantic import BaseModel, Field
from enum import StrEnum, auto
from typing import Optional

YEAR_MONTH_PATTERN = r"^\d{4}-(0[1-9]|1[0-2])$"


class PropertyType(StrEnum):
    CASH = auto()  # Gotówka

    # Obligacje skarbowe
    BOUNDS = auto()

    # Lokaty bankowe
    SAVINGS = auto()

    # Fundusze inwestycyjne
    ETF = auto()

    # Akcje
    STOCKS = auto()

    # Kryptowaluty
    CRYPTO = auto()


class Property(BaseModel):
    year_month_of_creation: str = Field(
        description="The year and month when the property was created in YYYY-MM format",
        pattern=YEAR_MONTH_PATTERN,
    )

    name: str = Field(
        description="The name of the property",
    )

    type: PropertyType = Field(
        description="The type of the property",
    )

    amount: float = Field(
        description="The amount of the property",
    )


class PropertyDB(Property):
    id_p: int = Field(
        description="The unique identifier of the property in the database",
    )


class PropertyFilter(BaseModel):
    type: Optional[PropertyType] = Field(
        default=None,
        description="The type of the property to filter by",
    )

    name: Optional[str] = Field(
        default=None,
        description="The name of the property to filter by",
    )

    year_month_of_creation_min: Optional[str] = Field(
        default=None,
        description="The minimum year and month of creation to filter by (YYYY-MM)",
        pattern=YEAR_MONTH_PATTERN,
    )

    year_month_of_creation_max: Optional[str] = Field(
        default=None,
        description="The maximum year and month of creation to filter by (YYYY-MM)",
        pattern=YEAR_MONTH_PATTERN,
    )

    creation_year: Optional[int] = Field(
        default=None,
        description="The creation year of the property to filter by",
    )

    creation_month: Optional[int] = Field(
        default=None,
        description="The creation month of the property to filter by",
    )

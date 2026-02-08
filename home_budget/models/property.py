from pydantic import BaseModel, Field
from datetime import datetime
from enum import StrEnum, auto
from typing import Optional


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
    creation_time: datetime = Field(
        description="The time when the property was created",
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

    creation_time_min: Optional[datetime] = Field(
        default=None,
        description="The minimum creation time of the property to filter by",
    )

    creation_time_max: Optional[datetime] = Field(
        default=None,
        description="The maximum creation time of the property to filter by",
    )

    creation_year: Optional[int] = Field(
        default=None,
        description="The creation year of the property to filter by",
    )

    creation_month: Optional[int] = Field(
        default=None,
        description="The creation month of the property to filter by",
    )

from home_budget.models.property import (
    Property,
    PropertyDB,
    PropertyFilter,
    PropertyType,
)
from datetime import datetime
from typing import List, Type, Self

from home_budget.db import Database


class PropertyRepository:
    @classmethod
    def select(
        cls: Type[Self], filter: PropertyFilter = PropertyFilter()
    ) -> List[PropertyDB]:
        connection = Database.connection()

        clauses: List[str] = []
        params: List[object] = []

        if filter.type is not None:
            clauses.append("type = ?")
            params.append(filter.type.value)

        if filter.name is not None:
            clauses.append("name = ?")
            params.append(filter.name)

        if filter.creation_time_min is not None:
            clauses.append("creation_time >= ?")
            params.append(filter.creation_time_min.isoformat())

        if filter.creation_time_max is not None:
            clauses.append("creation_time <= ?")
            params.append(filter.creation_time_max.isoformat())

        if filter.creation_year is not None:
            clauses.append("strftime('%Y', creation_time) = ?")
            params.append(f"{filter.creation_year:04d}")

        if filter.creation_month is not None:
            clauses.append("strftime('%m', creation_time) = ?")
            params.append(f"{filter.creation_month:02d}")

        query = "SELECT id_p, creation_time, name, type, amount FROM property"
        if clauses:
            query += " WHERE " + " AND ".join(clauses)

        cursor = connection.execute(query, params)
        rows = cursor.fetchall()

        return [
            PropertyDB(
                id_p=row[0],
                creation_time=datetime.fromisoformat(row[1]),
                name=row[2],
                type=PropertyType(row[3]),
                amount=row[4],
            )
            for row in rows
        ]

    @classmethod
    def insert(cls: Type[Self], property: Property) -> PropertyDB:
        connection = Database.connection()
        cursor = connection.execute(
            "INSERT INTO property (creation_time, name, type, amount) VALUES (?, ?, ?, ?)",
            (
                property.creation_time.isoformat(),
                property.name,
                property.type.value,
                property.amount,
            ),
        )
        connection.commit()

        return PropertyDB(id_p=cursor.lastrowid, **property.model_dump())

    @classmethod
    def delete(cls: Type[Self], id_p: int) -> bool:
        connection = Database.connection()
        cursor = connection.execute("DELETE FROM property WHERE id_p = ?", (id_p,))
        connection.commit()
        return cursor.rowcount > 0

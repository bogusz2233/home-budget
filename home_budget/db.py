import sqlite3
import threading
from pathlib import Path
from typing import Optional, Self, Type

from home_budget.config import CONFIG
from loguru import logger


class Database:
    _DB_LOCK = threading.Lock()
    _CONNECTION: Optional[sqlite3.Connection] = None

    @classmethod
    def _load_schema(cls) -> str:
        schema_path = Path(__file__).with_name("schemat.sql")

        if not schema_path.exists():
            raise FileNotFoundError(f"Database schema file not found: {schema_path}")

        return schema_path.read_text(encoding="utf-8")

    @classmethod
    def connection(cls) -> sqlite3.Connection:
        with cls._DB_LOCK:
            if cls._CONNECTION is None:
                cls._CONNECTION = sqlite3.connect(
                    CONFIG.DB_NAME, check_same_thread=False
                )

        return cls._CONNECTION

    @classmethod
    def initialize(cls: Type[Self]) -> None:
        schema = cls._load_schema()

        connection = cls.connection()
        connection.executescript(schema)
        connection.commit()
        cls._INITIALIZED = True


if __name__ == "__main__":
    Database.initialize()
    logger.success("Database initialized successfully")

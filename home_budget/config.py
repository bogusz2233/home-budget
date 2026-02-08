from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Final
from pathlib import Path


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    DEBUG: bool = Field(
        default=False,
        description="Enable debug mode",
    )
    VERBOSE: bool = Field(
        default=False,
        description="Enable verbose logging",
    )

    DB_NAME: Path = Field(
        default=Path("home_budget.sqlite"),
        description="The name of the database file",
    )


CONFIG: Final[Config] = Config()

from enum import Enum
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(str, Enum):
    DEV = "dev"
    STAGE = "stage"

    def __str__(self):
        return {
            self.DEV: "Dev",
            self.STAGE: "Stage"
        }[self]


class EnvironmentConfig(BaseSettings):
    restful_booker_url: str
    restful_booker_username: str
    restful_booker_password: str

    def __str__(self):
        return f"- Restful Booker API: {self.restful_booker_url}"

    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )


def load_config(env: Environment = Environment.DEV) -> EnvironmentConfig:
    env_file = Path(__file__).parent.parent / f".env.{env.value}"
    return EnvironmentConfig(_env_file=str(env_file))

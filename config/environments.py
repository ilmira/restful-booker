from dataclasses import dataclass
from enum import Enum


class Environment(str, Enum):
    DEV = "dev"
    STAGE = "stage"

    def __str__(self):
        return {
            self.DEV: "Dev",
            self.STAGE: "Stage"
        }[self]


@dataclass
class EnvironmentConfig:
    restful_booker_url: str

    def __str__(self):
        return f"- Restful Booker API: {self.restful_booker_url}"


environments = {
    Environment.DEV: EnvironmentConfig(
        restful_booker_url="https://restful-booker.herokuapp.com"
    ),
    Environment.STAGE: EnvironmentConfig(
        restful_booker_url="https://restful-booker.herokuapp.com"
    )
}

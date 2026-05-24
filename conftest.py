import pytest

from config.environments import Environment, environments, EnvironmentConfig
from services.restful_booker.auth.create_token import CreateToken
from services.restful_booker.booking.create_booking import CreateBooking
from services.restful_booker.booking.data import BodyBooking
from services.restful_booker.booking.delete_booking import DeleteBooking


def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="stage",
        help="Окружение для запуска тестов (dev/stage)"
    )


@pytest.fixture(scope="session")
def env(request) -> Environment:
    """Фикстура для получения текущего окружения"""
    env_name = request.config.getoption("--env")
    try:
        return Environment(env_name.lower())
    except ValueError:
        raise ValueError(
            f"Некорректное окружение: {env_name}. "
            f"Используйте одно из: dev/stage/prod"
        )


@pytest.fixture(scope="session")
def env_config(env) -> EnvironmentConfig:
    """Фикстура для получения конфигурации текущего окружения"""
    print(f"\nОкружение: {env}")
    print(f"{environments[env]}\n")
    return environments[env]


@pytest.fixture(scope="session")
def booking_id(env_config, authorize):
    response = CreateBooking(env_config).create_booking(BodyBooking.make_fake_body('full'))
    id = response.json()['bookingid']
    yield id
    DeleteBooking(env_config).delete_booking(id, authorize)



@pytest.fixture(scope='session')
def authorize(env_config):
    response = CreateToken(env_config).create_token({
        'username': 'admin',
        'password': 'password123'
    })
    yield response.json()['token']

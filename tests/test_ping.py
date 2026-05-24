import allure
import pytest
from services.restful_booker.ping.health_check import HealthCheck
from utils.helper import Helper


@allure.feature('Auth')
class TestPing:
    helper = Helper()

    @pytest.mark.smoke
    @allure.title('Проверка доступности API через пинг-запрос')
    @allure.testcase("https://example.com/testcase/16", "Test-16")
    def test_ping(self, env_config):
        with allure.step('Проверка доступности API через пинг-запрос'):
            response = HealthCheck(env_config).health_check()

        with allure.step('Проверяем статус код'):
            assert response.status_code == 201

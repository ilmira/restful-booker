import allure
import pytest
from faker import Faker

from services.restful_booker.auth.models.auth import AuthResponse
from services.restful_booker.auth.create_token import CreateToken
from utils.helper import Helper


@allure.feature('Auth')
class TestAuth:
    helper = Helper()

    @pytest.mark.smoke
    @allure.title('Успешная авторизация с валидными данными')
    @allure.testcase("https://example.com/testcase/1", "Test-1")
    def test_auth(self, env_config):
        login_user_data = {
            'username': 'admin',
            'password': 'password123'
        }
        with allure.step('Тест успешной авторизации пользователя'):
            response = CreateToken(env_config).create_token(login_user_data)
            self.helper.attach_response(response.json())

        with allure.step('Проверяем статус код'):
            assert response.status_code == 200
        with allure.step('Валидация схемы ответа'):
            validated_data = AuthResponse.model_validate(response.json())
            assert validated_data.token

    @pytest.mark.smoke
    @allure.title('Тест неуспешной авторизации')
    @allure.testcase("https://example.com/testcase/2", "Test-2")
    @pytest.mark.parametrize('login_data, name',
                             [({"username": Faker().user_name(),
                                "password": Faker().password()}, 'Авторизация с неверными учетными данными'),
                              ({"username": '',
                                "password": ''}, 'Авторизация с пустыми учетными данными'),
                              ({"password": 'password123'}, 'Авторизация без указания имени пользователя'),
                              ({"username": 'admin'}, 'Авторизация без указания пароля')])
    def test_not_valid_auth(self, env_config, login_data, name):
        with allure.step(name):
            response = CreateToken(env_config).create_token(login_data)
        with allure.step('Проверяем статус код'):
            assert response.status_code == 200
        with allure.step('Валидация схемы ответа'):
            validated_data = AuthResponse.model_validate(response.json())
            assert validated_data.reason

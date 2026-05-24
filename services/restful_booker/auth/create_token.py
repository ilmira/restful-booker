from services.base_api import BaseAPI


class CreateToken(BaseAPI):

    def __init__(self, env_config):
        """
        Args:
            env_config (EnvironmentConfig): Конфигурация окружения из фикстуры
        """
        super().__init__(base_url=env_config.restful_booker_url)

    def create_token(self, create_token_data):
        response = self.session.post(f"{self.base_url}/auth", json=create_token_data)
        return response
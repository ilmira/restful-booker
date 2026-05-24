from services.base_api import BaseAPI


class HealthCheck(BaseAPI):

    def __init__(self, env_config):
        """
        Args:
            env_config (EnvironmentConfig): Конфигурация окружения из фикстуры
        """
        super().__init__(base_url=env_config.restful_booker_url)

    def health_check(self):
        response = self.session.get(f"{self.base_url}/ping")
        return response

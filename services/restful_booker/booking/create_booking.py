from services.base_api import BaseAPI


class CreateBooking(BaseAPI):

    def __init__(self, env_config):
        """
        Args:
            env_config (EnvironmentConfig): Конфигурация окружения из фикстуры
        """
        super().__init__(base_url=env_config.restful_booker_url)

    def create_booking(self, data):
        """
           Создает новое бронирование
        """
        response = self.session.post(f"{self.base_url}/booking", json=data)
        return response

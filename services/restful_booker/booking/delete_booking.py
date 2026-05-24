from services.base_api import BaseAPI


class DeleteBooking(BaseAPI):

    def __init__(self, env_config):
        """
        Args:
            env_config (EnvironmentConfig): Конфигурация окружения из фикстуры
        """
        super().__init__(base_url=env_config.restful_booker_url)

    def delete_booking(self, id: int, token=None):
        """
           Удаляет бронирование по id
        """
        if token:
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Cookie": f'token={token}'
            }
        else:
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
        response = self.session.delete(f"{self.base_url}/booking/{id}", headers=headers)
        return response

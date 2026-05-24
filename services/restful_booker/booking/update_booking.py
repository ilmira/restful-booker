from services.base_api import BaseAPI

class UpdateBooking(BaseAPI):

    def __init__(self, env_config):
        """
        Args:
            env_config (EnvironmentConfig): Конфигурация окружения из фикстуры
        """
        super().__init__(base_url=env_config.restful_booker_url)

    def update_booking(self, id: int, data, token=None):
        """
           Обновляет все данные бронирования по id
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
        response = self.session.put(f"{self.base_url}/booking/{id}", json=data, headers=headers)
        return response

    def part_update_booking(self, id: int, data, token):
        """
           Обновляет часть данных бронирования по id
        """
        response = self.session.patch(f"{self.base_url}/booking/{id}", json=data, headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Cookie": f'token={token}'
        })
        return response

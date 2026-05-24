from services.base_api import BaseAPI


class GetBooking(BaseAPI):

    def __init__(self, env_config):
        """
        Args:
            env_config (EnvironmentConfig): Конфигурация окружения из фикстуры
        """
        super().__init__(base_url=env_config.restful_booker_url)

    def get_booking_by_id(self, id: int):
        """
           Возвращает бронирование по id
        """
        response = self.session.get(f"{self.base_url}/booking/{id}")
        return response

    def get_bookings(self):
        """
           Возвращает данные о бронированиях
        """
        response = self.session.get(f"{self.base_url}/booking")
        return response

    def get_bookings_by_firstname(self, firstname):
        """
           Возвращает данные о бронированиях с фильтрацией по firstname
        """
        response = self.session.get(f"{self.base_url}/booking?firstname={firstname}")
        return response

    def get_bookings_by_lastname(self, lastname):
        """
           Возвращает данные о бронированиях с фильтрацией по lastname
        """
        response = self.session.get(f"{self.base_url}/booking?lastname={lastname}")
        return response

    def get_bookings_by_checkin(self, checkin):
        """
           Возвращает данные о бронированиях с фильтрацией по checkin
        """
        response = self.session.get(f"{self.base_url}/booking?checkin={checkin}")
        return response

    def get_bookings_by_checkout(self, checkout):
        """
           Возвращает данные о бронированиях с фильтрацией по checkout
        """
        response = self.session.get(f"{self.base_url}/booking?checkout={checkout}")
        return response

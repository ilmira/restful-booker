from datetime import datetime, timedelta

import allure
import pytest
from faker import Faker

from services.restful_booker.booking.create_booking import CreateBooking
from services.restful_booker.booking.data import BodyBooking
from services.restful_booker.booking.delete_booking import DeleteBooking
from services.restful_booker.booking.get_booking import GetBooking
from services.restful_booker.booking.models.booking import BookingModelResponse, Booking, GetBookings
from services.restful_booker.booking.update_booking import UpdateBooking
from utils.helper import Helper


@allure.feature('Booking')
class TestBooking:
    helper = Helper()
    fake = Faker()

    @pytest.mark.smoke
    @allure.title('Успешное создание бронирования')
    @allure.testcase("https://example.com/testcase/3", "Test-3")
    @pytest.mark.parametrize('data_set', BodyBooking.make_fake_body('valid'))
    def test_create_booking(self, env_config, data_set):
        data, name = data_set
        with allure.step(name):
            response = CreateBooking(env_config).create_booking(data)
            self.helper.attach_response(response.json())

        with allure.step('Проверяем статус код'):
            assert response.status_code == 200
        with allure.step('Валидация схемы ответа'):
            validated_data = BookingModelResponse.model_validate(response.json())
            assert validated_data.bookingid
            assert validated_data.booking == Booking.model_validate(data)

    @pytest.mark.smoke
    @allure.title('Создание бронирования с некорректными датами')
    @allure.testcase("https://example.com/testcase/4", "Test-4")
    @pytest.mark.parametrize('data_set', BodyBooking.make_fake_body('not valid date'))
    def test_create_booking_not_valid_date(self, env_config, data_set):
        data, is_checkin = data_set
        with allure.step('Создание бронирования с некорректными датами'):
            response = CreateBooking(env_config).create_booking(data)
        with allure.step('Проверяем статус код'):
            assert response.status_code == 200
        with allure.step('Валидация схемы ответа'):
            validated_data = BookingModelResponse.model_validate(response.json())
            if is_checkin:
                assert validated_data.booking.bookingdates.checkin == '0NaN-aN-aN'
            else:
                assert validated_data.booking.bookingdates.checkout == '0NaN-aN-aN'

    @allure.title('Создание бронирования без обязательных полей')
    @allure.testcase("https://example.com/testcase/5", "Test-5")
    def test_create_booking_not_valid(self, env_config):
        with allure.step('Создание бронирования с некорректными датами'):
            response = CreateBooking(env_config).create_booking(BodyBooking.make_fake_body('not valid'))
        with allure.step('Проверяем статус код'):
            assert response.status_code == 500

    @pytest.mark.smoke
    @allure.title('Получение бронирования по корректному ID')
    @allure.testcase("https://example.com/testcase/6", "Test-6")
    def test_get_booking_by_id(self, env_config, booking_id):
        with allure.step('Получение бронирования по корректному ID'):
            response = GetBooking(env_config).get_booking_by_id(booking_id)
            self.helper.attach_response(response.json())

        with allure.step('Проверяем статус код'):
            assert response.status_code == 200
        with allure.step('Валидация схемы ответа'):
            Booking.model_validate(response.json())

    @pytest.mark.smoke
    @allure.title('Получение бронирования по несуществующему ID')
    @allure.testcase("https://example.com/testcase/7", "Test-7")
    def test_get_booking_not_valid_id(self, env_config):
        with allure.step('Получение бронирования по несуществующему ID'):
            response = GetBooking(env_config).get_booking_by_id(1000000000000000)

        with allure.step('Проверяем статус код'):
            assert response.status_code == 404

    @pytest.mark.smoke
    @allure.title('Получение списка всех бронирований')
    @allure.testcase("https://example.com/testcase/8", "Test-8")
    def test_get_bookings(self, env_config):
        with allure.step('Получение списка всех бронирований'):
            response = GetBooking(env_config).get_bookings()
            self.helper.attach_response(response.json())

        with allure.step('Проверяем статус код'):
            assert response.status_code == 200
        with allure.step('Валидация схемы ответа'):
            for data in response.json():
                GetBookings.model_validate(data)

    @pytest.mark.smoke
    @allure.title('Получение списка всех бронирований по имени')
    @allure.testcase("https://example.com/testcase/16", "Test-16")
    def test_get_bookings_by_firstname(self, env_config):
        with allure.step('Получение списка всех бронирований по имени'):
            my_first_name = self.fake.first_name()
            body = BodyBooking.make_fake_body('full')
            body["firstname"] = my_first_name
            CreateBooking(env_config).create_booking(body)
            response_firstname = GetBooking(env_config).get_bookings_by_firstname(my_first_name)

        for bookingid in response_firstname.json():
            validated_id = GetBookings.model_validate(bookingid)
            response = GetBooking(env_config).get_booking_by_id(validated_id.bookingid)
            self.helper.attach_response(response.json())
            with allure.step('Проверяем статус код'):
                assert response.status_code == 200
            with allure.step('Валидация схемы ответа и соответствия имени в ответе'):
                validated = Booking.model_validate(response.json())
                assert validated.firstname == my_first_name

    @pytest.mark.smoke
    @allure.title('Получение списка всех бронирований по фамилии')
    @allure.testcase("https://example.com/testcase/17", "Test-17")
    def test_get_bookings_by_lastname(self, env_config):
        with allure.step('Получение списка всех бронирований по фамилии'):
            my_last_name = self.fake.last_name()
            body = BodyBooking.make_fake_body('full')
            body["lastname"] = my_last_name
            CreateBooking(env_config).create_booking(body)
            response_lastname = GetBooking(env_config).get_bookings_by_lastname(my_last_name)

        for bookingid in response_lastname.json():
            validated_id = GetBookings.model_validate(bookingid)
            response = GetBooking(env_config).get_booking_by_id(validated_id.bookingid)
            self.helper.attach_response(response.json())
            with allure.step('Проверяем статус код'):
                assert response.status_code == 200
            with allure.step('Валидация схемы ответа и соответствия фамилии в ответе'):
                validated = Booking.model_validate(response.json())
                assert validated.lastname == my_last_name

    @pytest.mark.smoke
    @allure.title('Получение списка всех бронирований по дате заезда')
    @allure.testcase("https://example.com/testcase/18", "Test-18")
    def test_get_bookings_by_checkin(self, env_config):
        with allure.step('Получение списка всех бронирований по дате заезда'):
            my_checkin = self.fake.date()
            checkin_date = datetime.strptime(my_checkin, '%Y-%m-%d')
            checkout_date = checkin_date + timedelta(days=1)
            my_checkout = checkout_date.strftime('%Y-%m-%d')

            body = BodyBooking.make_fake_body('full')
            body['bookingdates']['checkin'] = my_checkin
            body['bookingdates']['checkout'] = my_checkout

            CreateBooking(env_config).create_booking(body)
            response_checkin = GetBooking(env_config).get_bookings_by_checkin(my_checkin)

        for bookingid in response_checkin.json():
            validated_id = GetBookings.model_validate(bookingid)
            response = GetBooking(env_config).get_booking_by_id(validated_id.bookingid)
            self.helper.attach_response(response.json())
            with allure.step('Проверяем статус код'):
                assert response.status_code == 200
            with allure.step('Валидация схемы ответа и соответствия даты заезда в ответе'):
                validated = Booking.model_validate(response.json())
                assert validated.bookingdates.checkin <= validated.bookingdates.checkout

    @pytest.mark.smoke
    @allure.title('Получение списка всех бронирований по дате выезда')
    @allure.testcase("https://example.com/testcase/19", "Test-19")
    def test_get_bookings_by_checkout(self, env_config):
        with allure.step('Получение списка всех бронирований по дате выезда'):
            my_checkout = self.fake.date()
            body = BodyBooking.make_fake_body('full')
            body['bookingdates']['checkout'] = my_checkout
            CreateBooking(env_config).create_booking(body)
            response_checkout = GetBooking(env_config).get_bookings_by_checkout(my_checkout)
        for bookingid in response_checkout.json():
            validated_id = GetBookings.model_validate(bookingid)
            response = GetBooking(env_config).get_booking_by_id(validated_id.bookingid)
            self.helper.attach_response(response.json())
            with allure.step('Проверяем статус код'):
                assert response.status_code == 200
            with allure.step('Валидация схемы ответа и соответствия даты выезда в ответе'):
                validated = Booking.model_validate(response.json())
                assert validated.bookingdates.checkout <= my_checkout

    @pytest.mark.smoke
    @allure.title('Полное успешное обновление бронирования')
    @allure.testcase("https://example.com/testcase/9", "Test-9")
    def test_update_booking(self, env_config, authorize, booking_id):
        with allure.step('Полное обновление бронирования'):
            body = BodyBooking.make_fake_body('full')
            response = UpdateBooking(env_config).update_booking(booking_id, body, authorize)
            self.helper.attach_response(response.json())
        with allure.step('Проверяем статус код'):
            assert response.status_code == 200
        with allure.step('Валидация схемы ответа'):
            Booking.model_validate(response.json())

    @pytest.mark.smoke
    @allure.title('Частичное успешное обновление бронирования')
    @allure.testcase("https://example.com/testcase/10", "Test-10")
    def test_part_update_booking(self, env_config, authorize, booking_id):
        with allure.step('Частичное обновление бронирования'):
            body = BodyBooking.make_fake_body('part')
            response = UpdateBooking(env_config).part_update_booking(booking_id, body, authorize)
            self.helper.attach_response(response.json())
        with allure.step('Проверяем статус код'):
            assert response.status_code == 200
        with allure.step('Валидация схемы ответа'):
            Booking.model_validate(response.json())

    @pytest.mark.smoke
    @allure.title('Неуспешное обновление бронирования')
    @allure.testcase("https://example.com/testcase/11", "Test-11")
    @pytest.mark.parametrize('token, name', [(None, 'Обновление бронирования без токена авторизации'),
                                             ('wrong_token', 'Обновление бронирования с неверным токеном')])
    def test_update_booking_not_valid_token(self, env_config, booking_id, token, name):
        with allure.step(name):
            body = BodyBooking.make_fake_body('full')
            response = UpdateBooking(env_config).update_booking(booking_id, body, token)

        with allure.step('Проверяем статус код'):
            assert response.status_code == 403

    @pytest.mark.smoke
    @allure.title('Обновление несуществующего бронирования')
    @allure.testcase("https://example.com/testcase/12", "Test-12")
    def test_part_update_booking_not_valid(self, env_config, authorize):
        with allure.step('Обновление несуществующего бронирования'):
            body = BodyBooking.make_fake_body('part')
            response = UpdateBooking(env_config).part_update_booking(10000000000000000, body, authorize)
        with allure.step('Проверяем статус код'):
            assert response.status_code == 405

    @pytest.mark.smoke
    @allure.title('Успешное удаление бронирования')
    @allure.testcase("https://example.com/testcase/13", "Test-13")
    def test_delete_booking(self, env_config, authorize, booking_id):
        with allure.step('Полное обновление бронирования'):
            response = DeleteBooking(env_config).delete_booking(booking_id, authorize)
        with allure.step('Проверяем статус код'):
            assert response.status_code == 201
        with allure.step('Проверяем корректное удаление бронирования'):
            assert GetBooking(env_config).get_booking_by_id(booking_id).status_code == 404

    @pytest.mark.smoke
    @allure.title('Неуспешное удаление бронирования')
    @allure.testcase("https://example.com/testcase/14", "Test-14")
    @pytest.mark.parametrize('token, name', [(None, 'Удаление бронирования без токена авторизации'),
                                             ('wrong_token', 'Удаление бронирования с неверным токеном')])
    def test_delete_booking_not_valid_token(self, env_config, booking_id, token, name):
        with allure.step(name):
            response = DeleteBooking(env_config).delete_booking(booking_id, token)

        with allure.step('Проверяем статус код'):
            assert response.status_code == 403

    @pytest.mark.smoke
    @allure.title('Удаление несуществующего бронирования')
    @allure.testcase("https://example.com/testcase/15", "Test-15")
    def test_delete_booking_not_valid(self, env_config, authorize):
        with allure.step('Обновление несуществующего бронирования'):
            response = DeleteBooking(env_config).delete_booking(10000000000000000, authorize)
        with allure.step('Проверяем статус код'):
            assert response.status_code == 405

from faker import Faker


class BodyBooking:

    @staticmethod
    def make_fake_body(body_type: str):
        fake = Faker()
        if body_type == 'valid':
            create_full_data = {
                "firstname": fake.first_name(),
                "lastname": fake.last_name(),
                "totalprice": fake.random_int(),
                "depositpaid": fake.boolean(),
                "bookingdates": {
                    "checkin": fake.date(),
                    "checkout": fake.date()
                },
                "additionalneeds": fake.word()
            }
            create_data_req = {
                "firstname": fake.first_name(),
                "lastname": fake.last_name(),
                "totalprice": fake.random_int(),
                "depositpaid": fake.boolean(),
                "bookingdates": {
                    "checkin": fake.date(),
                    "checkout": fake.date()
                }
            }
            return [(create_full_data, 'Создание бронирования со всеми полями'),
                    (create_data_req, 'Создание бронирования только с обязательными полями')]

        elif body_type == 'not valid date':
            create_data_not_valid_date_1 = {
                "firstname": fake.first_name(),
                "lastname": fake.last_name(),
                "totalprice": fake.random_int(),
                "depositpaid": fake.boolean(),
                "bookingdates": {
                    "checkin": 'april',
                    "checkout": fake.date()
                }
            }

            create_data_not_valid_date_2 = {
                "firstname": fake.first_name(),
                "lastname": fake.last_name(),
                "totalprice": fake.random_int(),
                "depositpaid": fake.boolean(),
                "bookingdates": {
                    "checkin": fake.date(),
                    "checkout": '2025/31/10'
                }
            }
            return [(create_data_not_valid_date_1, True), (create_data_not_valid_date_2, False)]
        elif body_type == 'not valid':
            create_data_not_valid = {
                "firstname": fake.first_name(),
                "lastname": fake.last_name(),
                "totalprice": fake.random_int(),
                "depositpaid": fake.boolean(),
                "bookingdates": {
                    "checkout": fake.date()
                }
            }
            return create_data_not_valid
        elif body_type == 'full':
            create_full_data = {
                "firstname": fake.first_name(),
                "lastname": fake.last_name(),
                "totalprice": fake.random_int(),
                "depositpaid": fake.boolean(),
                "bookingdates": {
                    "checkin": fake.date(),
                    "checkout": fake.date()
                },
                "additionalneeds": fake.word()
            }
            return create_full_data
        elif body_type == 'part':
            part_body = {
                "firstname": fake.first_name(),
                "lastname": fake.last_name()
            }
            return part_body

import allure
import json


class Helper:

    def attach_response(self, response):
        response = json.dumps(response, indent=4)
        allure.attach(body=response, name="API Response", attachment_type=allure.attachment_type.JSON)
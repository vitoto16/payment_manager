# Test library import
from unittest import TestCase

# Local imports
from payment_manager.api.api import app


class TestRequests(TestCase):
    def setUp(self):
        """Setting the app up for tests suite"""
        app.testing = True
        self.app = app.test_client()
        self.base_request_url = "/api/pay?client_id=1&buyer_name=Vittor&buyer_email=vittorvc@gmail.com&" \
                                "buyer_cpf=12345678910&payment_amount=1200&"

    def test_must_have_card_data_when_payment_type_is_card(self):
        request_url = self.base_request_url + "payment_type=card"

        response = self.app.post(request_url)

        self.assertEqual(400, response.status_code)

    def test_must_return_missing_arguments_on_response_error_message(self):
        """The response for this test will display all the missing arguments"""
        request_url = self.base_request_url + "payment_type=card&card_holder_name=Vittor&card_cvv=420"

        response = self.app.post(request_url)
        response = response.get_json()

        expected_response = "The arguments ['card_number', 'card_exp_date'] are required for this request."

        self.assertEqual(expected_response, response['message'])

    def test_boleto_success_response(self):
        request_url = self.base_request_url + "payment_type=boleto"

        response = self.app.post(request_url)

        expected_response = '"The boleto number is 123456789123456789"'

        self.assertEqual(expected_response, response.data.decode('utf-8').strip())

    def test_card_success_response(self):
        request_url = self.base_request_url + "payment_type=card&card_holder_name=Vittor&" \
                                              "card_number=1234567891011121&card_exp_date=69/69&card_cvv=420"

        response = self.app.post(request_url)

        expected_response = '"Transaction successful"'

        self.assertEqual(expected_response, response.data.decode('utf-8').strip())

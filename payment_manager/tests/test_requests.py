# Test library import
import unittest
from flask_testing import TestCase

# Local imports
from manage import app, db
from payment_manager.api.models import Client
from payment_manager.api.exceptions import MissingCardArgs


class TestRequests(TestCase):
    def create_app(self):
        app.config.from_object('payment_manager.api.config.TestingConfig')
        return app

    def setUp(self):
        """Setting the app up for tests suite"""
        self.app = app.test_client()
        self.base_request_url = "/pay/?client_id=1&buyer_name=Vittor&buyer_email=vittorvc@gmail.com&" \
                                "buyer_cpf=12345678910&payment_amount=1200&"
        db.create_all()
        db.session.add(Client())
        db.session.commit()

    def tearDown(self):
        db.session.close()
        db.drop_all()

    def test_must_have_card_data_when_payment_type_is_card(self):
        request_url = self.base_request_url + "payment_type=card"

        with self.assertRaises(MissingCardArgs):
            self.app.put(request_url)

    def test_must_return_missing_arguments_on_response_error_message(self):
        """The response for this test will display all the missing arguments"""

        request_url = self.base_request_url + "payment_type=card&card_holder_name=Vittor&card_cvv=420"

        expected_response = "The arguments ['card_number', 'card_exp_date'] are required for this request."

        with self.assertRaises(MissingCardArgs):
            response = self.app.put(request_url)
            response = response.get_json()
            self.assertEqual(expected_response, response['message'])

    def test_boleto_success_response(self):
        request_url = self.base_request_url + "payment_type=boleto"

        response = self.app.put(request_url)
        response = response.get_json()

        expected_response = "Your boleto number is 123456789123456789123456789"

        self.assertEqual(expected_response, response['message'])

    def test_card_success_response(self):
        request_url = self.base_request_url + "payment_type=card&card_holder_name=Vittor&" \
                                              "card_number=1234567891011121&card_exp_date=69/69&card_cvv=420"

        response = self.app.put(request_url)
        response = response.get_json()

        expected_response = "Your transaction was successful"

        self.assertEqual(expected_response, response['message'])


if __name__ == '__main__':
    unittest.main()

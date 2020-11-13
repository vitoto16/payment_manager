import os
import unittest

from flask_testing import TestCase

from manage import app
from payment_manager.api.config import basedir


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        app.config.from_object('payment_manager.api.config.Development')
        return app

    def test_app_is_development(self):
        self.assertTrue(app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///' + os.path.join(basedir, 'site.db'))
        self.assertTrue(app.config['DEBUG'] is True)


class TestTestingConfig(TestCase):
    def create_app(self):
        app.config.from_object('payment_manager.api.config.TestingConfig')
        return app

    def test_app_is_testing(self):
        self.assertTrue(app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite://')
        self.assertTrue(app.config['DEBUG'] is True)


if __name__ == '__main__':
    unittest.main()

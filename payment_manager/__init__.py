from flask_restx import Api
from flask import Blueprint

from .api.api import api as payment_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title="FLASK RESTX API BOILER-PLATE FOR PAYMENTS",
          version='1.0')

api.add_namespace(payment_ns, path='/pay')

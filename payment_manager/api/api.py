# Flask imports
from flask import request, jsonify

# Extension imports
from flask_restx import Resource

# Local imports
from .service import parser, save_new_payment
from .exceptions import MissingCardArgs
from payment_manager.api.util.pay_dto import PaymentDto

api = PaymentDto.api
_payment = PaymentDto.payment


@api.route('/')
class PaymentHandler(Resource):
    @api.doc("payment_data")
    @api.marshal_with(_payment)
    def get(self):
        return parser.parse_args(request)

    def put(self):
        arguments = parser.parse_args(request)

        return save_new_payment(arguments)


@api.errorhandler(MissingCardArgs)
def handle_missing_card_args(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


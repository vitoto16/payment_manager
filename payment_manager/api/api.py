# Flask imports
from flask import Flask, request, jsonify

# Extension imports
from flask_restx import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy

# Local imports
from payment_manager.config import Development
from payment_manager.api.exceptions import MissingCardArgs

app = Flask(__name__)
app.config.from_object(Development)

api = Api(app)
db = SQLAlchemy(app)

# Adding possible arguments for request parsing
parser = reqparse.RequestParser()
parser.add_argument('client_id', type=int, required=True)
parser.add_argument('buyer_name', required=True)
parser.add_argument('buyer_email', required=True)
parser.add_argument('buyer_cpf', required=True)
parser.add_argument('payment_amount', type=float, required=True)
parser.add_argument('payment_type', required=True, choices=['boleto', 'card'])
parser.add_argument('card_holder_name')
parser.add_argument('card_number')
parser.add_argument('card_exp_date')
parser.add_argument('card_cvv')


@api.route('/api/pay', methods=['GET', 'POST'])
class PaymentHandler(Resource):
    def get(self):
        return parser.parse_args(request)

    def post(self):
        arguments = parser.parse_args(request)
        if arguments.get('payment_type') == 'card':
            missing_args = self._check_card_data(arguments)
            if missing_args:
                raise MissingCardArgs(f"The arguments {missing_args} are required for this request.", status_code=400)
            else:
                return 'Transaction successful'
        elif arguments.get('payment_type') == 'boleto':
            return "The boleto number is 123456789123456789"

    @staticmethod
    def _check_card_data(arguments: dict):
        """Method for checking if card data is present on the request arguments
        when payment_type = 'card'"""
        card_arguments = ['card_holder_name', 'card_number', 'card_exp_date', 'card_cvv']
        for argument in card_arguments:
            if arguments[argument]:
                card_arguments.remove(argument)

        return card_arguments


@app.errorhandler(MissingCardArgs)
def handle_missing_card_args(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


if __name__ == '__main__':
    app.run(debug=True)

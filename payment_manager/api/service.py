from flask_restx import reqparse

# Local imports
from payment_manager.api import db
from payment_manager.api.exceptions import MissingCardArgs
from payment_manager.api.models import Client, Buyer, Payment, Card

# Adding possible data for request parsing
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


def save_new_payment(data):
    # If the client is in de database, process the request. If not, raise ValueError.
    client = Client.query.get(data['client_id'])
    if client:
        payment = Payment(amount=data['payment_amount'], pay_type=data['payment_type'])

        # If buyer is not in the database, create an object for further insertion
        buyer = Buyer.query.filter_by(cpf=data['buyer_cpf']).first()
        if not buyer:
            buyer = Buyer(name=data['buyer_name'], email=data['buyer_email'],
                          cpf=data['buyer_cpf'])

        # Establishes relationship with current client
        buyer.clients.append(client)
        buyer.payments.append(payment)
        db.session.add(buyer)

        # If the payment type is card and some card data is not present in the request, raise MissingCardArgs exception.
        # If all the data is present, process request.
        if data.get('payment_type') == 'card':
            missing_args = check_card_data(data)
            if missing_args:
                raise MissingCardArgs(f"The argument {missing_args} are required for this request.",
                                      status_code=400)
            else:
                # If card is not in the database, create an object for further insertion
                card = Card.query.filter_by(number=data['card_number']).first()
                if not card:
                    card = Card(owner_name=data['card_holder_name'], number=data['card_number'],
                                exp_date=data['card_exp_date'], cvv=data['card_cvv'])

            card.buyers.append(buyer)
            card.payments.append(payment)
            db.session.add(card)

        payment.client_id = client.id
        db.session.add(payment)
        db.session.commit()

        if payment.pay_type == 'card':
            response_object = {
                'status': 'Success',
                'message': 'Your transaction was successful',
            }
            return response_object, 200
        else:
            response_object = {
                'status': 'Success',
                'message': 'Your boleto number is 123456789123456789123456789',
            }
            return response_object, 200

    else:
        response_object = {
            'status': 'fail',
            'message': 'Client does not exist. Please send a valid id.',
        }
        return response_object, 400


def check_card_data(arguments: dict):
    """Method for checking if card data is present in the request arguments when
    payment_type = 'card'"""
    card_arguments = ['card_holder_name', 'card_number', 'card_exp_date', 'card_cvv']
    missing_args = list()
    for argument in card_arguments:
        if not arguments[argument]:
            missing_args.append(argument)

    return missing_args

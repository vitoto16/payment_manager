from flask_restx import Namespace, fields


class PaymentDto:
    api = Namespace('payment', description='payment related operations')
    payment = api.model('payment', {
        'amount': fields.Float(required=True, description='Payment amount'),
        'pay_type': fields.String(required=True, description='Payment type'),
        'status': fields.String(required=True, description='Payment status'),
        'client': fields.String(required=True, description='user Identifier')
    })

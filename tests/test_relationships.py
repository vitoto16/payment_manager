# Test library import
from unittest import TestCase

# Local imports
from payment_manager.api.api import app, db
from payment_manager.api.models import Client, Buyer, Card, Payment


class TestRelationships(TestCase):
    def setUp(self):
        """
        Creates a memory database for unit testing
        """
        app.config.from_object('payment_manager.config.Testing')
        db.create_all()
        db.session.add(Client())
        db.session.commit()

    def tearDown(self):
        db.session.close()
        db.drop_all()

    def test_client_and_buyer_relationship(self):
        client = Client.query.first()
        db.session.add(Buyer(name='Vittor', email='vittorvc@gmail.com', cpf='12345678910', clients=[client]))
        db.session.commit()

        buyer = Buyer.query.first()

        self.assertEqual('Vittor', client.buyers[0].name)
        self.assertEqual(1, buyer.clients[0].id)

    def test_buyer_and_card_relationship(self):
        db.session.add(Buyer(name='Vittor', email='vittorvc@gmail.com', cpf='12345678910'))
        db.session.commit()
        buyer = Buyer.query.first()

        db.session.add(Card(owner_name='Vittor', number='1234567891011121', exp_date='69/69',
                            cvv='420', buyers=[buyer]))
        db.session.commit()
        card = Card.query.first()

        self.assertEqual('Vittor', buyer.cards[0].owner_name)
        self.assertEqual('Vittor', card.buyers[0].name)

    def test_payment_client_and_buyer_relationships(self):
        client = Client.query.first()

        db.session.add(Buyer(name='Vittor', email='vittorvc@gmail.com', cpf='12345678910'))
        db.session.commit()
        buyer = Buyer.query.first()

        db.session.add(Payment(amount=1200.00, pay_type='Boleto', client_id=client.id, buyer_id=buyer.id))
        db.session.commit()
        payment = Payment.query.first()

        self.assertEqual(1, payment.client.id)
        self.assertEqual('Vittor', payment.buyer.name)

    def test_payment_and_card_relationship(self):
        client = Client.query.first()

        db.session.add(Buyer(name='Vittor', email='vittorvc@gmail.com', cpf='12345678910'))
        db.session.commit()
        buyer = Buyer.query.first()

        db.session.add(Card(owner_name='Vittor', number='1234567891011121', exp_date='69/69', cvv='420'))
        db.session.commit()
        card = Card.query.first()

        db.session.add(Payment(amount=1200.00, pay_type='Card', client_id=client.id, buyer_id=buyer.id, card=card))
        db.session.commit()
        payment = Payment.query.first()

        self.assertEqual(1, payment.card_id, "O ID do cartão está incorreto!")
        self.assertEqual(1, card.payments[0].id, "O ID do pagamento está incorreto!")

from . import db

buyers = db.Table('buyers',
                  db.Column('client_id', db.Integer, db.ForeignKey('client.id'), primary_key=True),
                  db.Column('buyer_id', db.Integer, db.ForeignKey('buyer.id'), primary_key=True),
                  )

cards = db.Table('cards',
                 db.Column('buyer_id', db.Integer, db.ForeignKey('buyer.id'), primary_key=True),
                 db.Column('card_id', db.Integer, db.ForeignKey('card.id'), primary_key=True),
                 )


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    buyers = db.relationship('Buyer', secondary=buyers, cascade='all, delete',
                             lazy='subquery', backref=db.backref('clients', lazy=True)
                             )

    payments = db.relationship('Payment', cascade='all, delete', backref=db.backref('client', lazy=True), lazy=True)

    def __repr__(self):
        return "Client()"


class Buyer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(35), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    cpf = db.Column(db.String(11), nullable=False, unique=True)

    cards = db.relationship('Card', secondary=cards, cascade='all, delete',
                            lazy='subquery', backref=db.backref('buyers', lazy=True)
                            )

    payments = db.relationship('Payment', cascade='all, delete', backref=db.backref('buyer', lazy=True), lazy=True)

    def __repr__(self):
        return f"Buyer(name={self.name}, email={self.email}, CPF={self.cpf})"


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_name = db.Column(db.String(35), nullable=False)
    number = db.Column(db.String(16), nullable=False, unique=True)
    exp_date = db.Column(db.String(5), nullable=False)
    cvv = db.Column(db.String(3), nullable=False)

    payments = db.relationship('Payment', cascade='all, delete', backref=db.backref('card', lazy=True), lazy=True)

    def __repr__(self):
        return f"Card(owner_name={self.owner_name}, number={self.number}, exp_date={self.exp_date}, cvv={self.cvv})"


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    pay_type = db.Column(db.String(6), nullable=False)
    status = db.Column(db.Boolean, default=False)

    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey('buyer.id'), nullable=False)
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'))

    def __repr__(self):
        return f"Payment(amount={self.amount}, pay_type={self.pay_type}," \
               f"client_id={self.client_id}, buyer_id={self.buyer_id})"

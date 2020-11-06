from flask import Flask
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

api = Api(app)
db = SQLAlchemy(app)

@api.route('/api/pay', methods=['GET', 'POST'])
class PaymentHandler(Resource):
    pass

if __name__ == '__main__':
    app.run(debug=True)
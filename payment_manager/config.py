class Development:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'

class Testing:
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
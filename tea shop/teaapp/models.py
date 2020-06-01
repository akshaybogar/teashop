import flask
from teaapp.alchemy_db import db
from werkzeug.security import generate_password_hash, check_password_hash

class UserModel(db.Model):
    __tablename__ = 'USERS'
    user_id = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String(30))
    lastname = db.Column(db.String(30))
    email = db.Column(db.String(30))
    password = db.Column(db.String(20))

    def __init__(self, user_id, firstname, lastname, email, password):
        self.user_id = user_id
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {'user_id':str(self.user_id), 'firstname':self.firstname,
         'lastname':self.lastname, 'email':self.email, 'password':self.password}

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def get_password(self, password):
        return check_password_hash(self.password, password)

    @classmethod
    def get(self):
        return [user.json() for user in UserModel.query.all()]

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, idx):
        return cls.query.filter_by(user_id=idx).first()


class ProductModel(db.Model):
    __tablename__ = 'PRODUCTS'
    product_id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(30))
    description = db.Column(db.String(30))
    amount = db.Column(db.Float(precision=2))

    def __init__(self, product_id, title, description, amount):
        self.product_id = product_id
        self.title =title
        self.description = description
        self.amount = amount

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {'product_id':str(self.product_id), 'title':self.title,
         'description':self.description, 'amount':str(self.amount)}

    @classmethod
    def get(self):
        return [product.json() for product in ProductModel.query.all()]

    @classmethod
    def find_by_id(cls, product_id):
            return (cls.query.filter_by(product_id=product_id).first())

class PurchaseModel(db.Model):
    __tablename__ = 'PURCHASE'
    product_id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, primary_key = True)

    def __init__(self, product_id, user_id):
        self.product_id = product_id
        self.user_id = user_id

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        return {'product_id':str(self.product_id), 'user_id': str(user_id)}

    @classmethod
    def get(self):
        return [item.json() for item in PurchaseModel.query.all()]

    @classmethod
    def find_by_product_user(cls, user_id, product_id):
        return cls.query.filter_by(user_id=user_id, product_id=product_id)

import os
from sqlalchemy import Column, String, Integer, Boolean, DateTime, create_engine
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json

database_name = "Zapoo"
database_path = "postgresql://{}/{}".format('postgres:PASSWORDHERE@localhost:5432', database_name)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)
    db.create_all()

class Category(db.Model):
    __tablename__ = 'category'
    category_id = db.Column(db.Integer, primary_key=True)
    catagory_name = db.Column(db.String(100))
    def insert(self):
        db.session.add(self)
        db.session.commit()
    def update(self):
        db.session.commit()

class Listing(db.Model):
    __tablename__ = 'listing'

    listing_id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100))
    address = db.Column(db.String(150))
    state = db.Column(db.String(4))
    city = db.Column(db.String(50))
    hours = db.Column(db.String(300))
    payment_type = db.Column(db.String(100))
    website_link = db.Column(db.String(300))
    phone = db.Column(db.String(10))
    keywords = db.Column(db.String(100))
    business_email = db.Column(db.String(150))
    description = db.Column(db.String(1000))
    layout_id = db.Column(db.Integer, default=0)
    style_id = db.Column(db.Integer, default=0)
    time_of_creation = db.Column(db.DateTime)
    cid = db.Column(db.Integer,db.ForeignKey(Category.category_id))
    categories = db.relationship('Category', backref=db.backref('listing'), lazy='joined')
    def insert(self):
        db.session.add(self)
        db.session.commit()
    def update(self):
        db.session.commit()
    def get_category_name(self):
        return Category.query.get(self.cid).catagory_name
    def delete(self):
        db.session.delete(self)
        db.session.commit()

class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(150))
    user_password = db.Column(db.String(500))
    user_is_active = db.Column(db.Boolean(),default=False)
    lid = db.Column(db.Integer,db.ForeignKey(Listing.listing_id))
    listings = db.relationship('Listing', backref=db.backref('user'), lazy='joined')

    def insert(self):
        db.session.add(self)
        db.session.commit()
    def update(self):
        db.session.commit()
    def get_listing(self):
        return Listing.query.get(self.lid)


class Email_Confirmation(db.Model):
    __tablename__ = 'email_confirmation'
    email_confirmation_id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(200),unique=True)
    is_confirmed = db.Column(db.Boolean(),default=False)
    uid = db.Column(db.Integer,db.ForeignKey(User.user_id))
    users = db.relationship('User', backref=db.backref('email_confirmation', cascade='all, delete'), lazy='joined')
    def insert(self):
        db.session.add(self)
        db.session.commit()
    def update(self):
        db.session.commit()

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(120)), nullable=False)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate


class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(120)), nullable=False)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate


class Show(db.Model):
    __tablename__ = "show"

    show_id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey(Venue.id))
    artist_id = db.Column(db.Integer, db.ForeignKey(Artist.id))
    start_time = db.Column(db.DateTime)
    artist = db.relationship('Artist', backref=db.backref('shows', cascade='all, delete'), lazy='joined')
    venue = db.relationship('Venue', backref=db.backref('shows', cascade='all, delete'), lazy='joined')
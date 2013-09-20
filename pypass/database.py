from __future__ import division
from passlib.hash import bcrypt
import googauth
import qrcode
import time
from datetime import datetime
import StringIO
from flask.ext.login import UserMixin

from pypass import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    domain = db.Column(db.String)
    password = db.Column(db.String)
    secret_key = db.Column(db.String)

    @property
    def qrcode(self):
        '''returns a stringio object containing
        the PNG qrcode for use in google authenticator
        '''
        qr = qrcode.QRCode(
              box_size=5,
              border=4,
          )
        qr.add_data(googauth.get_otpauth_url(
                                self.username, 
                                self.domain, 
                                self.secret_key
                                )
                            )
        qr.make(fit=True)
        barcode = StringIO.StringIO()
        qr.make_image().save(barcode)
        barcode.seek(0)
        return barcode

    def verify_pass(self, password):
        return bcrypt.verify(password, self.password)
    
    def verify_otp(self, otpass):
        ref_time = int(time.time()/30)
        check_time = googauth.verify_time_based(self.secret_key, otpass)
        return (ref_time == check_time)

    def __init__(self, username, domain, password):
        self.username = username
        self.domain = domain
        self.password = bcrypt.encrypt(password)
        self.secret_key = googauth.generate_secret_key()

    def __repr__(self):
        return '<User: {}>'.format(self.username)

class Credential(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    username = db.Column(db.String)
    password = db.Column(db.String)
    url = db.Column(db.String)
    notes = db.Column(db.Text)
    created = db.Column(db.DateTime)
    modified = db.Column(db.DateTime)

    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    owner = db.relationship('User',
                backref=db.backref('credentials', lazy='dynamic'))

    def __init__(self, title, username, password, owner):
        self.title = title
        self.username = username
        self.password = password
        self.modified = datetime.today()
        self.owner = owner

    def __repr__(self):
        return '<Credential: {0} @ {1}>'.format(self.title, self.modified)

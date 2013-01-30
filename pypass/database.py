from passlib.hash import bcrypt
import googauth
import qrcode
import time
from flask.ext.login import UserMixin

from pypass import db, domain

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    domain = db.Column(db.String)
    password = db.Column(db.String)
    secret_key = db.Column(db.String)

    @property
    def qrcode(self):
        '''returns a PIL image object containing 
        a qrcode for use in google authenticator'''
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
        return qr.make_image()

    def verify_pass(self, password):
        return bcrypt.verify(password, self.password)
    
    def verify_otp(self, otpass):
        ref_time = int(time.time()/30)
        check_time = googauth.verify_time_based(self.secret_key, otpass)
        return (ref_time == check_time)

    def __init__(self, username, password):
        self.username = username
        self.password = bcrypt.encrypt(password)
        self.secret_key = googauth.generate_secret_key()
        # this will eventually be submitted by the admin in a config file
        self.domain = 'pass.run107.com'

    def __repr__(self):
        return '<User: {}>'.format(self.username)

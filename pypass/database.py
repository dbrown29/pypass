from passlib.hash import bcrypt
import googauth

from pypass import db, domain

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    domain = db.Column(db.String)
    pass_hash = db.Column(db.String)
    secret_key = db.Column(db.String)

    @property
    def barcode_url(self):
        return googauth.get_barcode_url(
                            self.username, 
                            domain,
                            self.secret_key
                        )

    def __init__(self, username, password):
        self.username = username
        self.pass_hash = bcrypt.encrypt(password)
        self.secret_key = googauth.generate_secret_key()
        # this will eventually be submitted by the admin in a config file
        self.domain = 'pass.run107.com'

    def __repr__(self):
        return '<User: {}>'.format(self.username)

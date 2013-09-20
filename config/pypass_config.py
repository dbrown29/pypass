# config file for pypass app
SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/pypass.db'
SECRET_KEY = 'keepthisverysecret'

# this is used in generating the OTP
DOMAIN = 'pass.example.com'

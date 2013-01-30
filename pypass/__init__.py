from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

app = Flask(__name__)

# sqlalchemy setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/pypass.db'
db = SQLAlchemy(app)

# flask-login setup
lm = LoginManager()
lm.setup_app(app)

domain = 'pass.exit107.com'

# routes
import pypass.auth

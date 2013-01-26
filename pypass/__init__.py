from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

# sqlalchemy setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/pypass.db'
db = SQLAlchemy(app)

# normally these would come from the db but for the initial setup
user = 'dave.brown'
domain = 'pass.exit107.com'
secret_key = 'HA2TCNJRHBTDMNZY'

# routes
import pypass.auth

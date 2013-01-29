from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

# sqlalchemy setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/pypass.db'
db = SQLAlchemy(app)

domain = 'pass.exit107.com'

# routes
import pypass.auth

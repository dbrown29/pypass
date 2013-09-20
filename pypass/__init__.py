from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

app = Flask(__name__)

# make sure the env_var 'PYPASS_CONFIG' is set to the path
# for the config file
app.config.from_envvar('PYPASS_CONFIG')

# sqlalchemy setup
db = SQLAlchemy(app)

# flask-login setup
lm = LoginManager()
lm.setup_app(app)

# routes
from pypass.routes import auth
from pypass.routes import passdb

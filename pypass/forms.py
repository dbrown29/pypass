from flask.ext.wtf import Form
from wtforms import TextField
from wtforms.validators import DataRequired

class LoginForm(Form):
    username = TextField('username', validators=[DataRequired()])
    password = TextField('password', validators=[DataRequired()])
    otpass = TextField('one time password', validators=[DataRequired()])

class CreateUserForm(Form):
    username = TextField('username', validators=[DataRequired()])
    password = TextField('password', validators=[DataRequired()])

class CreateEntryForm(Form):
    title = TextField('title', validators=[DataRequired()])
    username = TextField('username', validators=[DataRequired()])
    password = TextField('password', validators=[DataRequired()])

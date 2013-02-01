from flask.ext.wtf import Form, TextField, Required

class LoginForm(Form):
    username = TextField('username', validators=[Required()])
    password = TextField('password', validators=[Required()])
    otpass = TextField('one time password', validators=[Required()])

class CreateUserForm(Form):
    username = TextField('username', validators=[Required()])
    password = TextField('password', validators=[Required()])

class CreateEntryForm(Form):
    title = TextField('title', validators=[Required()])
    username = TextField('username', validators=[Required()])
    password = TextField('password', validators=[Required()])

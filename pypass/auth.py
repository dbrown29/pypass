from __future__ import division
from flask import abort, request, session, url_for, render_template, redirect, send_file
import StringIO
from sqlalchemy.orm.exc import NoResultFound
from flask.ext.login import login_user, logout_user, current_user, login_required

from pypass import app, db, lm
from pypass.database import User
from pypass.forms import LoginForm, CreateUserForm

@lm.user_loader
def load_user(userid):
    return User.query.get(userid)

@app.route('/login/', methods=['POST','GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # make sure the user exists
        username = form.username.data
        password = form.password.data
        otpass = str(form.otpass.data)
        try:
           user = User.query.filter(User.username==username).one() 
        except NoResultFound:
            abort(404)

        # verify code and password, then login user
        if user.verify_otp(otpass) and user.verify_pass(password):
            login_user(user)
            return redirect(url_for('profile', username=user.username))

    return render_template('login.html', form=form)

@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/create/', methods=['POST','GET'])
def create_user():
    form = CreateUserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('profile', username=user.username))

    return render_template('create_user.html', form=form)

@app.route('/profile/<username>/')
@login_required
def profile(username):
    try:
        user = User.query.filter(User.username==username).one()
    except NoResultFound:
        abort(404)
    return render_template('user_profile.html', user=user)

@app.route('/barcode/')
@login_required
def barcode():
    barcode = StringIO.StringIO()
    current_user.qrcode.save(barcode)
    barcode.seek(0)
    return send_file(barcode)

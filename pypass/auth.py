from __future__ import division
from time import time
import googauth
import qrcode
import PIL
import StringIO
from flask import abort, request, session, url_for, render_template, redirect
from flask import send_file
from passlib.hash import bcrypt
from sqlalchemy.orm.exc import NoResultFound

from pypass import app, db
from pypass.database import User

#@app.route('/', methods=['POST', 'GET'])
#def verify_code():
#  if request.method == 'POST':
#    code = str(request.form['code'])
#
#    ref_time = int(time()/30)
#    check_time = googauth.verify_time_based(secret_key, code)
#
#    if check_time == ref_time:
#      return render_template('check_auth.html', verify=True)
#    else:
#      return render_template('check_auth.html', verify=False)
#  else:
#    return render_template('check_auth.html', verify=False)

@app.route('/', methods=['POST','GET'])
def user_auth():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        code = str(request.form['code'])

        # make sure the user exists
        try:
           user = User.query.filter(User.username==username).one() 
        except NoResultFound:
            abort(404)

        # verify code and password, then return
        ref_time = int(time()/30)
        check_time = googauth.verify_time_based(user.secret_key, code)
        user_verify = bcrypt.verify(password, user.pass_hash)
        if (ref_time == check_time) and user_verify:
            return render_template('check_auth.html', verify=True)
        else:
            return render_template('check_auth.html', verify=False)
    else:
        # nothing submitted yet, present form
        return render_template('check_auth.html', verify=False)

@app.route('/create/', methods=['POST','GET'])
def create_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return render_template('create_user.html', user=user)
    else:
        return render_template('create_user.html')

@app.route('/profile/<username>/')
def user_profile(username):
    try:
        user = User.query.filter(User.username==username).one()
    except NoResultFound:
        abort(404)
    return render_template('user_profile.html', user=user)

@app.route('/barcode/<username>/')
def barcode_img(username):
    try:
        user = User.query.filter(User.username==username).one()
    except NoResultFound:
        abort(404)
    barcode = StringIO.StringIO()
    qr = qrcode.QRCode()
    qr.add_data(googauth.get_otpauth_url(
                            user.username, 
                            user.domain, 
                            user.secret_key
                            )
                        )
    qr.make(fit=True)
    img_data = qr.make_image()
    img_data.save(barcode)
    barcode.seek(0)
    return send_file(barcode)

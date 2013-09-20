from flask import abort, request, session, url_for, render_template, redirect, send_file
from sqlalchemy.orm.exc import NoResultFound
from flask.ext.login import login_user, logout_user, current_user, login_required

from pypass import app, db
from pypass.database import User, Credential
from pypass.forms import CreateEntryForm

@app.route('/cipher/create/', methods=['POST', 'GET'])
@login_required
def create_entry():
    form = CreateEntryForm()
    if form.validate_on_submit():
           title = form.title.data
           username = form.username.data
           password = form.password.data
           domain = app.config['DOMAIN']
           entry = Credential(
                      title=title, 
                      username=username,
                      domain=domain,
                      password=password,
                      owner=current_user,
                  )
           db.session.add(entry)
           db.session.commit()
           return redirect(url_for('list_entry'))

    return render_template('create_entry.html', form=form)

@app.route('/cipher/list/')
@login_required
def list_entry():
    return render_template('list_entry.html', entries=current_user.credentials.all())

from __future__ import division
from time import time
import googauth
from flask import abort, request, session, url_for, render_template, redirect

from pypass import app, db

# should normally come from the db
from pypass import user, domain, secret_key


@app.route('/', methods=['POST', 'GET'])
def verify_code():
  if request.method == 'POST':
    code = str(request.form['code'])

    ref_time = int(time()/30)
    check_time = googauth.verify_time_based(secret_key, code)

    if check_time == ref_time:
      return render_template('check_auth.html', verify=True)
    else:
      return render_template('check_auth.html', verify=False)
  else:
    return render_template('check_auth.html', verify=False)

# for now, use the defaults set in the config file
#config_filename = '.pypassrc'
#config = SafeConfigParser()
#config.read([config_filename])
#
#if not config.has_section('auth'):
#    user = 'dave.brown'
#    domain = 'pass.exit107.com'
#    secret_key = googauth.generate_secret_key()
#    config.set('auth', 'user', user)
#    config.set('auth', 'domain', domain)
#    config.set('auth', 'secret_key', secret_key)
#else:
#    user = config.get('auth', 'user')
#    domain = config.get('auth', 'domain')
#    secret_key = config.get('auth', 'secret_key')
#
#with open(config_filename, 'w') as fh:
#    config.write(fh)



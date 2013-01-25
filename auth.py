from __future__ import division
from time import time
from ConfigParser import SafeConfigParser

import googauth

# for now, use the defaults set in the config file
config_filename = '.pypassrc'
config = SafeConfigParser()
config.read([config_filename])

if not config.has_section('auth'):
    user = 'dave.brown'
    domain = 'pass.exit107.com'
    secret_key = googauth.generate_secret_key()
    config.set('auth', 'user', user)
    config.set('auth', 'domain', domain)
    config.set('auth', 'secret_key', secret_key)
else:
    user = config.get('auth', 'user')
    domain = config.get('auth', 'domain')
    secret_key = config.get('auth', 'secret_key')

with open(config_filename, 'w') as fh:
    config.write(fh)

# check otp keys
while True:
    code = raw_input('code in > ')
    ref_time = int(time()/30)
    check_time = googauth.verify_time_based(secret_key, code)
    if check_time == ref_time:
        print 'success'
        print check_time
        print ref_time
    else:
        print 'failed'
        print check_time
        print ref_time

from pypass import app

from werkzeug import SharedDataMiddleware
import os

# serve the static files from flask for dev work
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
  '/': os.path.join(os.path.dirname(__file__), '/static')
})

app.debug = True
app.secret_key = 'keepthisverysecret'
app.run(host='0.0.0.0', port=5000)

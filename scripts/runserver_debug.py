import os
import sys

# add pypass to the path
app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(app_path)

# configuration path, normally set in an enviromental variable
config_path = os.path.abspath(os.path.join(app_path, 'config', 'pypass_config.py'))
os.environ['PYPASS_CONFIG'] = config_path

# now we can import the app
from pypass import app
from werkzeug import SharedDataMiddleware

# serve the static files from flask for dev work
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
  '/': os.path.join(os.path.dirname(__file__), '/static')
})

app.debug = True
app.run(host='0.0.0.0', port=5000)

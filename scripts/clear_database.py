import os
import sys

# add pypass to the path
app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(app_path)

# configuration path, normally set in an enviromental variable
config_path = os.path.abspath(os.path.join(app_path, 'config', 'pypass_config.py'))
os.environ['PYPASS_CONFIG'] = config_path

# now we can import it
from pypass import app, database

# drop and build the db
print('dropping all tables')
database.db.drop_all()

print('building all tables')
database.db.create_all()

print('done, now run runserver_debug.py')

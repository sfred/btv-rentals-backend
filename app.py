from api.search import Search
from flask import Flask, make_response
from flask_restful import Api
from utils.config import config
from utils.json import DateTimeEncoder
from waitress import serve
import json
import utils.db as db
import sys

app = Flask(__name__)
api = Api(app)

# Resource routing
api.add_resource(Search, '/search/<term>')

# Load existing database schema
db.init_db()
metadata = db.get_metadata()

if ('addresses' not in metadata.tables.keys()
        or 'properties' not in metadata.tables.keys()):
    print(("One or more tables is not present in the database."
           "Have you run the pipeline yet?"
           ))
    sys.exit(1)

# Implement our custom DateTimeEncoder
@api.representation('application/json')
def output_json(data, code, headers=None):
    resp = make_response(json.dumps(data, cls=DateTimeEncoder), code)
    return resp


if __name__ == '__main__':
    if config['FLASK_ENV'] == 'development':
        app.run()
    else:
        open('/tmp/app-initialized', 'w').close()
        serve(app, unix_socket='/tmp/nginx.socket')

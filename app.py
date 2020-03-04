from flask import Flask, request, Response
from flask_restful import reqparse, Api, Resource
from utils.config import config
from waitress import serve
import json

app = Flask(__name__)
api = Api(app)

# parser arguments
parser = reqparse.RequestParser()
parser.add_argument('term')

# Endpoints
class Search(Resource):
    def get(self, term):
        return {'searched': term}

# Setup the Api resource routing here
api.add_resource(Search, '/search/<term>')

if __name__ == '__main__':
    open('/tmp/app-initialized', 'w').close()
    if config['FLASK_ENV'] == 'development':
        app.run()
    else:
        serve(app, unix_socket='/tmp/nginx.socket')
from flask import Flask, request, Response
from flask_restful import reqparse, Api, Resource
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
    app.run(debug=True)
from api.search import Search
from flask import Flask
from flask_restful import Api
from utils.config import config
from waitress import serve

app = Flask(__name__)
api = Api(app)

# Resource routing
api.add_resource(Search, '/search/<term>')

if __name__ == '__main__':
    if config['FLASK_ENV'] == 'development':
        app.run()
    else:
        open('/tmp/app-initialized', 'w').close()
        serve(app, unix_socket='/tmp/nginx.socket')

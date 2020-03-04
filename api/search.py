from flask_restful import reqparse, Resource


class Search(Resource):
    def get(self, term):
        # Parser arguments
        parser = reqparse.RequestParser()
        parser.add_argument('term')

        return {'searched': term}

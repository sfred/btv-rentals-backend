from flask_restful import Resource
from scourgify import normalize_address_record
from scourgify.exceptions import UnParseableAddressError
import utils.db as db


class Search(Resource):
    def get(self, term):
        try:
            term = normalize_address_record(term)['address_line_1']
        except UnParseableAddressError:
            return {'error': 'Address not parseable'}, 400

        addresses = db.get_metadata().tables['addresses']
        properties = db.get_metadata().tables['properties']

        session = db.create_session()

        query = session.query(properties) \
            .join(addresses, addresses.c.Span == properties.c.Span) \
            .filter(addresses.c.Address == term) \
            .all()

        properties = []
        for row in query:
            properties.append(dict(row._asdict()))

        if len(properties) == 0:
            return {'error': 'No results found'}, 404
        else:
            return properties

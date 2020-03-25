from api.cache import cache
from flask import request
from flask_restful import Resource
from scourgify import normalize_address_record
from scourgify.exceptions import UnParseableAddressError
import urllib.parse
import utils.db as db


def search_cache_key():
    args = request.args
    key = request.path + '?' + urllib.parse.urlencode([
        (k, v) for k in sorted(args) for v in sorted(args.getlist(k))
    ])
    return key


class Search(Resource):
    @cache.cached(timeout=600, key_prefix=search_cache_key)
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
            return {'properties': properties}

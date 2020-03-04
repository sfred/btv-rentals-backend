from datetime import date, datetime
import json


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, date) or isinstance(o, datetime):
            return o.isoformat()

        return super().default(o)

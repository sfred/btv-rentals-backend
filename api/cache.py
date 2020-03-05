from flask_caching import Cache
from utils.config import config

cache = Cache(config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': config['REDIS_URL']
})

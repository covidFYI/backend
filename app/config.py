import os

class Config(object):

    SECRET_KEY = os.urandom(30)
    MONGODB_SETTINGS = {
        'db'  : os.environ.get("MONGODB_NAME",'covidfyi'),
        'host': os.environ.get("MONGODB_HOST", '127.0.0.1'),
        'port': int(os.environ.get("MONGODB_PORT", 27017))
    }

    CACHE_CONFIG = {
        'CACHE_TYPE'       : 'redis',
        'CACHE_REDIS_HOST' : os.environ.get("REDIS_HOST", 'localhost'),
        'CACHE_REDIS_PORT' : 6379
    }
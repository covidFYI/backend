import os

class Config(object):

    SECRET_KEY = os.urandom(30)
    MONGODB_SETTINGS = {
        'db': 'covidfyi',
        'host': '127.0.0.1',
        'port': 27017
    }

    CACHE_CONFIG = {
        'CACHE_TYPE' : 'redis'
    }

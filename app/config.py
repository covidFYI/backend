import os

class Config(object):

    SECRET_KEY = os.urandom(30)
    
    MONGO_URI = 'mongodb://localhost:27017/covidfyi'
    MONGO_DBNAME = 'covidfyi'

    CACHE_CONFIG = {
        'CACHE_TYPE' : 'redis'
    }

import os

class Config(object):

    SECRET_KEY = os.urandom(30)
    SCHEDULER_API_ENABLED = True
    
    MONGO_URI = 'mongodb://localhost:27017/covidfyi_2'
    MONGO_DBNAME = 'covidfyi_2'

    CACHE_CONFIG = {
        'CACHE_TYPE' : 'redis'
    }

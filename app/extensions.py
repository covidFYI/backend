from flask_mongoengine import MongoEngine 
from flask_caching import Cache

db = MongoEngine()
cache = Cache(config={'CACHE_TYPE': 'redis'})

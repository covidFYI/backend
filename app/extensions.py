from flask_caching import Cache
from flask_pymongo import PyMongo


mongo = PyMongo()
cache = Cache(config={'CACHE_TYPE': 'redis'})

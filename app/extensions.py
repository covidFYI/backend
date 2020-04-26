from flask_caching import Cache
from flask_pymongo import PyMongo
from flask_apscheduler import APScheduler

scheduler = APScheduler()
mongo     = PyMongo()
cache     = Cache()

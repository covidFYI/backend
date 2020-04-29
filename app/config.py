import os
from datetime import timedelta

MONGO_HOST = os.getenv('MONGO_HOST', 'localhost')
DB_NAME    = os.getenv('DB_NAME', 'covidfyi')

class Config(object):

    SECRET_KEY = os.urandom(30)
    SCHEDULER_API_ENABLED = True
        
    MONGO_URI    = f'mongodb://{MONGO_HOST}:27017/{DB_NAME}'
    MONGO_DBNAME = DB_NAME

    CACHE_CONFIG = {
        'CACHE_TYPE' : 'redis'
    }

    CELERY_BROKER_URL     = f'redis://localhost:6379/1'
    CELERY_RESULT_BACKEND = f'redis://localhost:6379/1'

    CELERY_BEAT_TASKS = {
        'update_db_periodic': {
            'task': 'update_db_12hrs',
            'schedule': timedelta(hours=12)
        }
    }

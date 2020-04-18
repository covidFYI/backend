from app import cache
from app.data import data_bp
from app.data.models import Entries
from app.extensions import cache
from flask import jsonify, request, make_response, abort, Response
from flask_caching import Cache
import json

CACHE_TIMEOUT = 60*1 # 1 min

@data_bp.route('/api/v1/states')
@cache.cached(timeout=CACHE_TIMEOUT, key_prefix='states')
def states():

    states = Entries.objects.distinct('state')

    return Response(json.dumps({
        'states': states,
    }), mimetype='application/json')

@data_bp.route('/api/v1/state/<string:state>')
@cache.memoize(timeout=CACHE_TIMEOUT)
def state(state):
    
    entries = tuple(Entries.objects(state=state))

    return jsonify({'entries' : entries})

@data_bp.route('/api/v1/state/<string:state>/<string:category>')
@cache.memoize(timeout=CACHE_TIMEOUT)
def state_w_category(state, category):

    entries = tuple(Entries.objects(state=state, category=category))

    return jsonify({'entries' : entries})

@data_bp.route('/api/v1/stats')
@cache.cached(timeout=CACHE_TIMEOUT, key_prefix='stats')
def stat():

    categories = tuple(Entries.objects.distinct('category'))
    stats = {
        category: Entries.objects(category=category).count() for category in categories
    }
    
    return Response(json.dumps({
        'stats': stats,
    }), mimetype='application/json')

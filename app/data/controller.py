from app import cache
from app.data import data_bp
from app.extensions import cache, mongo
from flask import jsonify, request, make_response, abort, Response
from flask_caching import Cache
import json
from random import shuffle
CACHE_TIMEOUT = 1*1 # 10 min

entries_collection = mongo.db.entries
news_collection = mongo.db.news
    
@data_bp.route('/api/v1/states')
@cache.cached(timeout=CACHE_TIMEOUT, key_prefix='states')
def states():

    entries = entries_collection.find({}, {'state':1}).distinct('state')
    entries = tuple(entries)
    return jsonify({
        'result': entries
    })


@data_bp.route('/api/v1/news')
@cache.cached(timeout=CACHE_TIMEOUT, key_prefix='news')
def news():
    news = news_collection.find({}, {'_id': 0})
    news = tuple(news)
    return jsonify({
        'result': news 
    })

@data_bp.route('/api/v1/categories')
@cache.cached(timeout=CACHE_TIMEOUT, key_prefix='categories')
def infotypes():
    entries = entries_collection.find({}, {'category': 1}).distinct('category')
    entries = tuple(entries)
    return jsonify({
        'result': entries
    })

@data_bp.route('/api/v1/categories/total')
@cache.cached(timeout=CACHE_TIMEOUT, key_prefix='total_categories')
def infotypes_total():
    pipeline = [{"$group": {"_id": "$category", "total": {"$sum": 1}}}]
    total = entries_collection.aggregate(pipeline) 

    res = tuple({'category':x['_id'], 'total': x['total']} for x in total)
    return jsonify({
        'result': res
    })


@data_bp.route('/api/v1/categories/<category>/total')
@cache.cached(timeout=CACHE_TIMEOUT, key_prefix='total_categories_state')
def infotypes_total_state(category):
    pipeline = [{"$match" : { "category" : category} },
                {"$group": {"_id": "$state", "total": {"$sum": 1}}}]
    total = entries_collection.aggregate(pipeline)
    print(category)
    res = tuple({'category': x['_id'], 'total': x['total']} for x in total)
    return jsonify({
        'result': res
    }) 
    

@data_bp.route('/api/v1/state/<string:state>')
@cache.memoize(timeout=CACHE_TIMEOUT)
def state_view(state):

    entries = entries_collection.find({'state': state}, {'_id':0})
    return jsonify({
        'result': entries
    })

@data_bp.route('/api/v1/state/<string:state>/<string:category>')
@cache.memoize(timeout=CACHE_TIMEOUT)
def state_w_category(state, category):

    entries = entries_collection.find({'state':state, 'category':category}, {'_id':0})
    entries = tuple(entries)
    return jsonify({
        'result': entries
    })



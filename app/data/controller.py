from app import cache
from app.data import data_bp
from app.extensions import cache, mongo
from flask import jsonify, request, make_response, abort, Response
from flask_caching import Cache
from requests import get
import json
from random import shuffle

CACHE_TIMEOUT = 60*10 # 10 min

news_collection    = mongo.db.news
entries_collection = mongo.db.entries

""" CovidFYI Data APIs """

@data_bp.route('/api/v1/states')
@cache.cached(timeout=CACHE_TIMEOUT, key_prefix='states')
def states():

    entries = entries_collection.find({}, {'state':1}).distinct('state')
    entries = tuple(entries)

    return jsonify({
        'results': entries
    })

@data_bp.route('/api/v1/categories')
@cache.cached(timeout=CACHE_TIMEOUT, key_prefix='categories')
def categories():

    entries = entries_collection.find({}, {'category': 1}).distinct('category')
    entries = tuple(entries)

    return jsonify({
        'results': entries
    })

@data_bp.route('/api/v1/state/<string:state>')
@cache.memoize(timeout=CACHE_TIMEOUT)
def state_view(state):

    entries = tuple(entries_collection.find({'state': state}, {'_id':0}))

    return jsonify({
        'results': entries
    })

@data_bp.route('/api/v1/state/<string:state>/<string:category>')
@cache.memoize(timeout=CACHE_TIMEOUT)
def state_w_category(state, category):

    entries = entries_collection.find({'state':state, 'category':category}, {'_id':0})
    entries = tuple(entries)

    return jsonify({
        'results': entries
    })


""" CovidFYI Data stats """

@data_bp.route('/api/v1/categories/total')
@cache.cached(timeout=CACHE_TIMEOUT, key_prefix='total_categories')
def categories_total():

    pipeline = [{"$group": {"_id": "$category", "total": {"$sum": 1}}}]
    total = entries_collection.aggregate(pipeline) 

    result = tuple({'category':x['_id'], 'total': x['total']} for x in total)
    
    return jsonify({
        'results': result
    })

@data_bp.route('/api/v1/categories/<category>/total')
@cache.memoize(timeout=CACHE_TIMEOUT)
def categories_total_state(category):

    pipeline = [{"$match" : { "category" : category} },
                {"$group": {"_id": "$state", "total": {"$sum": 1}}}]
    total = entries_collection.aggregate(pipeline)

    result = tuple({'state': x['_id'], 'total': x['total']} for x in total)

    return jsonify({
        'category': category,
        'results'  : result
    }) 
    

""" Covid news """

@data_bp.route('/api/v1/news')
@cache.cached(timeout=CACHE_TIMEOUT, key_prefix='news')
def news():
    
    news = news_collection.find({}, {'_id': 0})
    news = tuple(news)

    return jsonify({
        'results': news 
    })


""" India Covid stats """

@data_bp.route('/api/v1/covid_stats')
@cache.cached(timeout=CACHE_TIMEOUT, key_prefix='stats')
def covid_stats():

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
    }

    resp = get('https://api.covid19india.org/data.json', headers=headers)

    json_data = resp.json()
    recent_data = json_data['cases_time_series'][-1]
    
    stats = [{'Confirmed': recent_data['totalconfirmed']},
        {'Recovered' : recent_data['totalrecovered']},
        {'Deaths': recent_data['totaldeceased']}]

    return jsonify(stats)


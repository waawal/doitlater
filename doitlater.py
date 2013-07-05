from os import environ
import datetime
try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

import gevent
gevent.monkey.patch_all()

import requests
import logbook
import parsedatetime
from bottle import Bottle, route, request, HTTPError

TOKENS = environ.get('doitlater')
if TOKENS is None:
    raise EnvironmentError('Could not find a doitlater\
        environment variable filled with yummy tokens')
TOKENS = TOKENS.split(':')

app = Bottle()

def execute(req):
    if not req['request'].get('auth') is None:
        req['request']['auth'] = req['request']['auth'].split(':')
    res = requests.request(req['request'].get('method', 'GET'),
                           req['request']['url'],
                           auth=req['request'].get('auth'),
                           data=req['request'].get('body'),
                           )
    if req['request'].get('callback'):
        requests.post(req['request']['callback'], data=res)

def difference_in_seconds(stamp):
    delta = stamp - datetime.datetime.now()
    return (24*60*60*delta.days + delta.seconds + delta.microseconds/1000000)

def enqueue(req):
    if req['when'] is None:
        gevent.spawn(execute, req)
    stamp = parsedatetime.Calendar().parse(req['when'])
    when = difference_in_seconds(stamp)
    if when < 0:
        gevent.spawn(execute, req)

    gevent.spawn_later(when, execute, req)

def validate_request(req):
    if 'request' not in req or not req['request'].get('url'):
        raise HTTPError(400)
    try:
        urlparse(req['request']['url'])
    except ValueError:
        raise HTTPError(400)
    validated = {}
    for key in "body when hook".split():
        validated[key] = req.get(key)
    for key in "url method auth headers".split()
        validated['request'][key] = req['request'].get(key)
    enqueue(validated)

@app.route('/<token>/')
def index(token):
    if not token in TOKENS:
        raise HTTPError(401)
    if request.json:
        validate_request(request.json)
    else:
        validate_request(request.params)

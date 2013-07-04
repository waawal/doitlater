from os import environ
import datetime

import gevent
gevent.monkey.patch_all()

import requests
from bottle import Bottle, route, request, HTTPError 

TOKENS = environ.get('doitlater')
if TOKENS is None:
    raise EnvironmentError('Could not find a doitlater\
        environment variable filled with yummy tokens')
TOKENS = TOKENS.split(':')

app = Bottle()

def difference_in_seconds(stamp):
    delta = stamp - datetime.datetime.now()
    return (24*60*60*delta.days + delta.seconds + delta.microseconds/1000000)

def enqueue(req):
    gevent.spawn_later(seconds, function, *args, **kwargs)

def validate_request(req):
    pass

@app.route('/<token>/')
def index(token):
    if not token in TOKENS:
        raise HTTPError(401)
    if request.json:
        validate_request(request.json)
    else:
        validate_request(request.params)

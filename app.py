#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from os import environ as env
from sys import argv

import bottle
from bottle import default_app, request, route, response, get

bottle.debug(True)
application = bottle.default_app()
if __name__ == "__main__":
    bottle.run(application, host="0.0.0.0", port=argv[1])


@get("/")
def index():
    response.content_type = "text/plain; charset=utf-8"
    ret = "Hello world, I'm %s!\n\n" % os.getpid()
    ret += "Request vars:\n"
    for k, v in request.environ.items():
        if 'bottle.' in k:
            continue
        ret += '%s=%s\n' % (k, v)

    ret += "\n"
    ret += "Environment vars:\n"

    for k, v in env.items():
        if "bottle." in k:
            continue
        ret += "%s=%s\n" % (k, v)

    return ret


@get("/db")
def db():
    response.content_type = "text/plain; charset=utf-8"
    import tsc.db
    conn = tsc.db.connect()
    out = str(conn.thread_id())
    return out

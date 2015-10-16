#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from os import environ as env
from sys import argv

import bottle
from bottle import default_app, request, route, response, get

bottle.debug(True)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host='0.0.0.0', port=argv[1])

@get('/')
def index():
    response.content_type = 'text/plain; charset=utf-8'
    ret =  'Hello world, I\'m %s!\n\n' % os.getpid()
    ret += 'Request vars:\n'
    for k, v in request.environ.items():
        if 'bottle.' in k:
            continue
        ret += '%s=%s\n' % (k, v)

    ret += '\n'
    ret += 'Environment vars:\n'

    for k, v in env.items():
        if 'bottle.' in k:
            continue
        ret += '%s=%s\n' % (k, v)

    return ret

# if __name__ == '__main__':
#     app.log.debug("config = %s" % app.config)
#     #app.log.debug("routes = %s" % app.routes)
#     if app.config['debug']:
#         routes_debug = ''
#         # TODO: 関数が定義されているファイル名も表示する
#         for route in app.routes:
#             routes_debug += "%6s %s\n" % (route.method, route.rule)
#         #self.router.add(route.rule, route.method, route, name=route.name)
#         #inspect.getargspec(func)
#         app.log.debug("===== routes =====\n" + routes_debug)
#
#     port = os.environ.get('PORT')
#     if port:
#         config['port'] = port
#     run(app, **config)

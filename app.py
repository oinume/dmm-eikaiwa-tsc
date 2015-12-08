#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from sys import argv
import bottle
from bottle import default_app, request, route, response, get
from tsc.models import connect

bottle.debug(True)
application = bottle.default_app()
if __name__ == "__main__":
    bottle.run(application, host="0.0.0.0", port=argv[1])


@get("/")
def index():
    response.content_type = "application/json; charset=utf-8"
    try:
        conn = connect()
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM teacher")
            cursor.fetchone()
        return {
            "APP_ID": os.environ.get("APP_ID"),
            "db": "true",
        }
    finally:
        if conn:
            conn.close()


@get("/db")
def db():
    response.content_type = "text/plain; charset=utf-8"
    import tsc.db
    conn = tsc.db.connect()
    out = str(conn.thread_id())
    return out

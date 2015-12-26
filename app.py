#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from sys import argv
import bottle
from bottle import template, response, get
from tsc.models import DB

bottle.debug(True)
application = bottle.default_app()
if __name__ == "__main__":
    bottle.run(application, host="0.0.0.0", port=argv[1])


@get("/")
def index():
    html = """
<html>
<head>
<meta charset="UTF-8"></meta>
<title>dmm-eikaiwa-tsc - Teacher Schedule Checker for DMM Eikaiwa</title>
</head>
<body>
Want to know how to use this app? See <a href="https://github.com/oinume/dmm-eikaiwa-tsc/blob/master/README.md">README</a>

<script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-2241989-17', 'auto');
  ga('send', 'pageview');
</script>
</body>
</html>
    """
    return template(html)



@get("/status")
def status():
    response.content_type = "application/json; charset=utf-8"
    conn = None
    try:
        conn = DB.connect(os.environ.get("CLEARDB_DATABASE_URL"))
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

import enum
import os
import urllib.parse
import pymysql
import pymysql.cursors

# Register database schemes in URLs.
urllib.parse.uses_netloc.append("mysql")


ScheduleStatus = enum.Enum("ScheduleStatus", "reservable reserved finished")


def connect() -> pymysql.connections.Connection:
    url_env = os.environ.get("CLEARDB_DATABASE_URL")
    if not url_env:
        raise Exception("Environment 'CLEARDB_DATABASE_URL' is not defined.")
    url = urllib.parse.urlparse(url_env)
    return pymysql.connect(
        host=url.hostname,
        user=url.username,
        password=url.password,
        database=url.path[1:],
        charset="utf8mb4",
        autocommit=True,
        cursorclass=pymysql.cursors.DictCursor)

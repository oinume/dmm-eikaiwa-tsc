from concurrent.futures import Future
from requests_futures.sessions import FuturesSession
from tsc.models import Teacher


class Tracker:

    def __init__(self, app_id: str) -> None:
        self._app_id = app_id
        self._session = FuturesSession()

    def send_async(self, teacher: Teacher) -> Future:
        payload = {
            "v": 1,
            "tid": "UA-2241989-17",
            "cid": 555,
            "t": "pageview",
            "dh": self._app_id,
            "dp": teacher.id,
            "dt": teacher.name,
        }
        return self._session.post("http://www.google-analytics.com/collect", payload)

    def close(self) -> None:
        self._session.close()

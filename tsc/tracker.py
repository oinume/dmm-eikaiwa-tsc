import requests

class Tracker:

    def __init__(self, app_id: str):
        self.app_id = app_id

    def send(self, teacher_id):
        session = requests.Session()
        data = {
            
        }
        session.post(
            "http://www.google-analytics.com/collect",
            {

            }
        )

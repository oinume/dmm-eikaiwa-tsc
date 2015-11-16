from tsc.models import *
import datetime
from pprint import pprint
import json

def test_diff_schedules():
    old = [
        Schedule(1, datetime.datetime(2015, 11, 1, 22, 00), ScheduleStatus.reservable).to_json(),
        Schedule(1, datetime.datetime(2015, 11, 1, 23, 00), ScheduleStatus.reservable).to_json(),
    ]
    new = [
        Schedule(1, datetime.datetime(2015, 11, 1, 22, 00), ScheduleStatus.reserved).to_json(),
        Schedule(1, datetime.datetime(2015, 11, 1, 23, 00), ScheduleStatus.reservable).to_json(),
        Schedule(1, datetime.datetime(2015, 11, 2, 11, 00), ScheduleStatus.reservable).to_json(),
    ]
    # TODO: extract only reservable record. get_new_reservable_schedules()
    # " + {"datetime": "2015-11-02 11:00:00", "status": "reservable", "teacher_id": 1}"
    for di in diff_schedules(old, new):
        print("line:", di)
    assert 1 == 2

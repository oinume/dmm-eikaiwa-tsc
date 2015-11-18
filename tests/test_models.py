from tsc.models import *
import datetime


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
    schedules = Schedule.get_new_reservable_schedules(old, new)
    assert len(schedules) == 1

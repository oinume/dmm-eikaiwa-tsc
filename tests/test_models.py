from tsc.models import *
import datetime


def test_get_new_reservable_schedules():
    old = [
        Schedule(1, datetime.datetime(2015, 11, 1, 22, 00), ScheduleStatus.reservable),
        Schedule(1, datetime.datetime(2015, 11, 1, 23, 00), ScheduleStatus.reservable),
    ]
    new = [
        Schedule(1, datetime.datetime(2015, 11, 1, 22, 00), ScheduleStatus.reserved),
        Schedule(1, datetime.datetime(2015, 11, 1, 23, 00), ScheduleStatus.reservable),
        Schedule(1, datetime.datetime(2015, 11, 2, 11, 00), ScheduleStatus.reservable),
        Schedule(1, datetime.datetime(2015, 11, 2, 11, 30), ScheduleStatus.reserved),
    ]
    schedules = Schedule.get_new_reservable_schedules(old, new)
    assert schedules == [
        Schedule(1, datetime.datetime(2015, 11, 2, 11, 00), ScheduleStatus.reservable)
    ]

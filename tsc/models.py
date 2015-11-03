import datetime
import enum


class Teacher:

    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name


ScheduleStatus = enum.Enum("ScheduleStatus", "reservable reserved finished")


class Schedule:

    def __init__(self, teacher_id: int, dt: datetime.datetime, status: ScheduleStatus):
        self.teacher_id = teacher_id
        self.datetime = dt
        self.status = status

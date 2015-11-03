import datetime
import enum


class Teacher:

    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

    # def get_name(self):
    #     return self._name
    #
    # def set_name(self, value):
    #     self._name = value
    #
    # name = property(get_name, set_name, None, "'name' property")


ScheduleStatus = enum.Enum("ScheduleStatus", "reservable reserved finished")


class Schedule:

    def __init__(self, teacher_id: int, datetime: datetime.datetime, status: ScheduleStatus):
        self.teacher_id = teacher_id
        self.datetime = datetime
        self.status = status

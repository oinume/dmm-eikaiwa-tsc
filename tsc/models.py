import datetime
import enum
from typing import List

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


class DBMapper:

    def __init__(self, conn):
        self._conn = conn

    def update_teacher(self, teacher: Teacher):
        with self._conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO teacher VALUES (%s, %s) ON DUPLICATE KEY UPDATE name=%s",
                (teacher.id, teacher.name, teacher.name,)
            )

    def update_schedules(self, schedules: List[Schedule]):
        if not schedules:
            return
        with self._conn.cursor() as cursor:
            values = []
            sql = "INSERT INTO schedule VALUES"
            for schedule in schedules:
                sql += " (%s, %s, %s),"
                values.extend([schedule.teacher_id, str(schedule.datetime), schedule.status.value])
            sql = sql[:-1]
            sql += " ON DUPLICATE KEY UPDATE status=VALUES(status)"
            cursor.execute(sql, values)

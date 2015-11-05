import datetime
import enum
from typing import List

class Teacher:

    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

    def __repr__(self) -> str:
        return "<Teacher({0}, {1})>".format(self.id, self.name)


ScheduleStatus = enum.Enum("ScheduleStatus", "reservable reserved finished")


class Schedule:

    def __init__(self, teacher_id: int, dt: datetime.datetime, status: ScheduleStatus):
        self.teacher_id = teacher_id
        self.datetime = dt
        self.status = status

    def __repr__(self) -> str:
        return "<Schedule({0}, {1}, {2})>".format(self.teacher_id, self.datetime, self.status.name)


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

    def find_schedules(
        self,
        teacher_id: int,
        from_date: datetime.date,
        to_date:datetime.date
    ) -> List[Schedule]:
        with self._conn.cursor() as cursor:
            sql = """
SELECT * FROM schedule
WHERE
  teacher_id = %s
  AND DATE(datetime) BETWEEN %s AND %s
""".strip()
            cursor.execute(
                sql,
                (teacher_id, from_date.strftime("%Y-%m-%d"), to_date.strftime("%Y-%m-%d"))
            )
            print(cursor._last_executed)

            schedules = []
            for row in cursor.fetchall():
                schedules.append(Schedule(row["teacher_id"], row["datetime"], ScheduleStatus(row["status"])))
            return schedules

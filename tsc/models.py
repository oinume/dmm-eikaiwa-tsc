import datetime
import difflib
import enum
import github
import json
import pymysql
import pymysql.cursors
from typing import List
import urllib.parse
# Register database schemes in URLs.
urllib.parse.uses_netloc.append("mysql")


class Teacher:

    def __init__(self, id: int, name: str) -> None:
        self.id = id
        self.name = name

    def __repr__(self) -> str:
        return "<Teacher({}, {})>".format(self.id, self.name)


ScheduleStatus = enum.Enum("ScheduleStatus", "reservable reserved finished")


class Schedule:

    def __init__(self, teacher_id: int, dt: datetime.datetime, status: ScheduleStatus) -> None:
        self.teacher_id = teacher_id
        self.datetime = dt
        self.status = status

    def __repr__(self) -> str:
        return "<Schedule({}, {}, {})>".format(self.teacher_id, self.datetime, self.status.name)

    def __eq__(self, other) -> bool:
        return str(self) == str(other)

    @classmethod
    def get_new_reservable_schedules(
        cls, old_schedules: List["Schedule"], new_schedules: List["Schedule"]
    ) -> List["Schedule"]:
        old = [o.to_json() for o in old_schedules]
        new = [o.to_json() for o in new_schedules]

        differ = difflib.Differ()
        ret = []
        diffs = list(differ.compare(old, new))
        for i, d in enumerate(diffs):
            if d.startswith("+ "):
                if (i == len(diffs) - 1) or (i < len(diffs) - 1 and not diffs[i+1].startswith("? ")):
                    schedule = cls.from_json(d[1:])
                    if schedule.status == ScheduleStatus.reservable:
                        ret.append(schedule)
            #print("line{}:{}".format(i, d))
        return ret

    @classmethod
    def from_json(cls, json_str) -> "Schedule":
        d = json.loads(json_str)
        return cls(d["teacher_id"], d["datetime"], ScheduleStatus[d["status"]])

    def to_json(self) -> str:
        d = {
            "teacher_id": self.teacher_id,
            "datetime": self.datetime.strftime("%Y-%m-%d %H:%M:%S"),
            "status": self.status.name
        }
        return json.dumps(d)


class DB:

    def __init__(self, conn):
        self._conn = conn

    @classmethod
    def connect(cls, database_url: str) -> pymysql.connections.Connection:
        url = urllib.parse.urlparse(database_url)
        return pymysql.connect(
            host=url.hostname,
            user=url.username,
            password=url.password,
            database=url.path[1:],
            charset="utf8mb4",
            autocommit=True,
            cursorclass=pymysql.cursors.DictCursor)

    def update_teacher(self, teacher: Teacher) -> None:
        with self._conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO teacher VALUES (%s, %s) ON DUPLICATE KEY UPDATE name=%s",
                (teacher.id, teacher.name, teacher.name,)
            )

    def update_schedules(self, schedules: List[Schedule]) -> None:
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
        to_date: datetime.date
    ) -> List[Schedule]:
        with self._conn.cursor() as cursor:
            sql = """
SELECT * FROM schedule
WHERE
  teacher_id = %s
  AND DATE(datetime) BETWEEN %s AND %s
ORDER BY datetime
""".strip()
            cursor.execute(
                sql,
                (teacher_id, from_date.strftime("%Y-%m-%d"),
                 (to_date + datetime.timedelta(days=2)).strftime("%Y-%m-%d"))
            )
            #print(cursor._last_executed)

            schedules = []
            for row in cursor.fetchall():
                schedules.append(Schedule(row["teacher_id"], row["datetime"], ScheduleStatus(row["status"])))
            return schedules


class GitHub:

    def __init__(self, token: str=None):
        self.client = github.Github(token)

    def get_latest_tag(self) -> str:
        repo = self.client.get_repo("oinume/dmm-eikaiwa-tsc")
        tags = list(repos.get_tags())
        if len(tags) == 0:
            return None  # TODO: Use Optional
        return tags[0].name

# coding: utf-8
import copy
import datetime
import lxml.html
import re
import requests
from typing import Any, List, Tuple

from tsc.log import logger
from tsc.models import Schedule, ScheduleStatus, Teacher


class TeacherScheduleFetcher:
    def __init__(self):
        self._session = requests.Session()
        self._session.mount("http://", requests.adapters.HTTPAdapter(max_retries=3))

    def fetch(self, teacher_id: int) -> Tuple[Teacher, List[Any]]:
        logger.debug("Getting teacher_id={0} schedules from eikaiwa.dmm.com".format(teacher_id))
        url_base = "http://eikaiwa.dmm.com/teacher/index/{0}/"
        url = url_base.format(teacher_id)
        res = self._session.get(url, timeout=5)
        if res.status_code != 200:
            raise(Exception("fetch error: url={0}, status={1}".format(url, res.status_code)))

        root = lxml.html.fromstring(res.text)
        title = root.xpath("//title")[0].text
        name = title.split("-")[0].strip()
        teacher = Teacher(teacher_id, name)

        # schedule, reservation
        original_date = datetime.date.today()
        date = copy.copy(original_date)
        time_items = root.xpath("//ul[@class='oneday']//li")
        schedules = []
        logger.debug("--- teacher id={0}, name={1} ---".format(teacher_id, name))
        for time_item in time_items:
            time_class = time_item.attrib["class"]
            text = time_item.text_content().strip()
            # print("{time_class}:{text}".format(**locals()))
            # blank, reservable, reserved
            if time_class == "date":
                match = re.match(r"([\d]+)月([\d]+)日(.+)", text)
                if match:
                    original_date = date.replace(date.year, int(match.group(1)), int(match.group(2)))
                    date = copy.copy(original_date)
            elif time_class.startswith("t-") and text != "":
                tmp = time_class.split("-")
                hour, minute = int(tmp[1]), int(tmp[2])
                if hour >= 24:
                    # 24:30 -> 00:30
                    hour -= 24
                    if date == original_date:
                        # Set date to next day for 24:30
                        date += datetime.timedelta(days=1)
                dt = datetime.datetime(date.year, date.month, date.day, hour, minute, 0, 0)
                if text == "終了":
                    status = "finished"
                elif text == "予約済":
                    status = "reserved"
                elif text == "予約可":
                    status = "reservable"
                else:
                    raise(Exception("Unknown schedule text:{0}".format(text)))

                logger.debug("dt={dt}, status={status}".format(**locals()))
                schedule = Schedule(teacher.id, dt, ScheduleStatus[status])
                schedules.append(schedule)
            else:
                pass
        return teacher, schedules

    def close(self):
        self._session.close()

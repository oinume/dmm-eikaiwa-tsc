# coding: utf-8
import datetime
import re

from selenium import webdriver
import lxml.html
import tsc.db
from tsc.models import Teacher
from typing import Any, List, Tuple


class TeacherScheduleFetcher:
    def __init__(self):
        self.browser = webdriver.PhantomJS()
        #self.browser = webdriver.Firefox()
        self.conn = tsc.db.connect()

    def fetch(self, teacher_id: int) -> Tuple[Teacher, List[Any]]:
        url_base = "http://eikaiwa.dmm.com/teacher/index/{0}/"
        b = self.browser
        b.get(url_base.format(teacher_id))

        root = lxml.html.fromstring(b.page_source)
        title = root.xpath("//title")[0].text
        name = title.split("-")[0].strip()
        teacher = Teacher(teacher_id, name)

        # schedule, reservation
        date = datetime.date.today()
        time_items = root.xpath("//ul[@class='oneday']//li")
        schedules = []
        for time_item in time_items:
            time_class = time_item.attrib["class"]
            text = time_item.text_content().strip()
            #print("{time_class}:{text}".format(**locals()))
            # blank, reservable, reserved
            if time_class == "date":
                match = re.match(r"([\d]+)月([\d]+)日(.+)", text)
                if match:
                    date = date.replace(date.year, int(match.group(1)), int(match.group(2)))
            elif time_class.startswith("t-") and text != "":
                tmp = time_class.split("-")
                dt = datetime.datetime(date.year, date.month, date.day, int(tmp[1]), int(tmp[2]), 0, 0)
                if text == "終了":
                    status = "finished"
                elif text == "予約済":
                    status = "reserved"
                elif text == "予約可":
                    status = "reservable"
                else:
                    raise(Exception("Unknown schedule text:{0}".format(text)))
                print("{dt}:{status}".format(**locals()))
                schedules.append({
                    "datetime": dt,
                    "status": status,
                })
            else:
                pass
        return teacher, schedules

    def close(self):
        self.conn.close()
        self.browser.quit()

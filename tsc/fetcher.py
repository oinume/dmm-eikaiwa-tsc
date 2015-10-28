# coding: utf-8
import datetime
import re

from selenium import webdriver
import lxml.html
import tsc.db


class TeacherScheduleFetcher:

    def __init__(self):
        self.browser = webdriver.PhantomJS()
        #self.browser = webdriver.Firefox()
        self.conn = tsc.db.connect()

    def fetch(self, teacher_id):
        url_base = "http://eikaiwa.dmm.com/teacher/index/{0}/"
        b = self.browser
        b.get(url_base.format(teacher_id))

        root = lxml.html.fromstring(b.page_source)
        title = root.xpath("//title")[0].text
        name = title.split("-")[0].strip()
        with self.conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO teacher VALUES (%s, %s) ON DUPLICATE KEY UPDATE name=%s",
                (teacher_id, name, name,)
            )

        date = datetime.date.today()
        time_items = root.xpath("//ul[@class='oneday']//li")
        for time_item in time_items:
            time_class = time_item.attrib["class"]
            text = time_item.text_content().strip()
            #print("{time_class}:{text}".format(**locals()))
            # blank, reservable, reserved
            #date_str = ""
            if time_class == "date":
                match = re.match(r"([\d]+)月([\d]+)日(.+)", text)
                if match:
                    date = date.replace(date.year, int(match.group(1)), int(match.group(2)))
                    #print(date)
            elif time_class.startswith("t-") and text != "":
                tmp = time_class.split("-")
                dt = datetime.datetime(date.year, date.month, date.day, int(tmp[1]), int(tmp[2]), 0, 0)
                status = "reservable" if text == "予約済" else "reserved"
                print("{dt}:{status}".format(**locals()))
                # TODO: INSERT TO DB or append list
            else:
                #print("else")
                pass

    def close(self):
        self.conn.close()
        self.browser.quit()

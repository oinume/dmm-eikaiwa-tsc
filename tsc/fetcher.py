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
            print("{time_class}:{text}".format(**locals()))
            # blank, reservable, reserved
            #date_str = ""
            if time_class == "date":
                match = re.match(r"([\d]+)月([\d]+)日(.+)", text)
                if match:
                    #print(match.group(1), match.group(2))
                    date = date.replace(date.year, int(match.group(1)), int(match.group(2)))
                    print(date)
                #print(date_str)
            elif time_class.startswith("t-"):
                tmp = time_class.split("-")
                tmp[1], tmp[2]
            else:
                pass

        """
        t-22-30:予約済
        t-23-00:
        t-23-30:
        t-24-00:
        t-24-30:
        t-25-00:
        t-25-30:
        date:10月28日(水)
        """

    def close(self):
        self.conn.close()
        self.browser.quit()

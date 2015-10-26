# coding: utf-8
from selenium import webdriver
import lxml.html
import tsc.db
from pprint import pprint

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

        times = root.xpath("//ul[@class='oneday']//li")
        for time in times:
            print("time = ", time.text.strip(), time.attrib["class"])
        #pprint(date)


    def close(self):
        self.conn.close()
        self.browser.quit()

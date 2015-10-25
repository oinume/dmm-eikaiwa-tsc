# coding: utf-8
from selenium import webdriver
from pyquery import PyQuery
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
        d = PyQuery(b.page_source)
        title = d("title").text()
        name = title.split("-")[0].strip()
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO teacher VALUES (%s, %s) ON DUPLICATE KEY UPDATE name=%s",
            (teacher_id, name, name,)
        )

    def close(self):
        self.conn.close()
        self.browser.quit()

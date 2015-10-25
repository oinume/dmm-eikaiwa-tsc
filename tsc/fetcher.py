# coding: utf-8
from selenium import webdriver
from pyquery import PyQuery as pq


class TeacherScheduleFetcher:

    def __init__(self):
        self.browser = webdriver.PhantomJS()
        #self.browser = webdriver.Firefox()

    def fetch(self, teacher_id):
        url_base = "http://eikaiwa.dmm.com/teacher/index/{0}/"
        b = self.browser
        b.get(url_base.format(teacher_id))
        d = pq(b.page_source)
        title = d("title").text()
        print(title)
        # TODO: insert to teacher table


    def close(self):
        self.browser.quit()


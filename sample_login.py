#!/usr/bin/env python
# encoding: utf-8

import os

from selenium import webdriver
from pprint import pprint

driver = webdriver.PhantomJS()
#driver = webdriver.Firefox()
driver.get("https://www.dmm.com/my/-/login/=/path=DRVESVwZTldRDlBRRFdIUwwIGFVfVEs_")
login_id = driver.find_element_by_id("login_id")
login_id.send_keys(os.environ["DMM_LOGIN_ID"])
password = driver.find_element_by_id("password")
password.send_keys(os.environ["DMM_LOGIN_PASSWORD"])
driver.find_element_by_tag_name("form").submit()
print(driver.page_source)

driver.quit()

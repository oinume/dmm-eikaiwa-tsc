#!/usr/bin/env python

from pyquery import PyQuery as pq
import requests

payload = {
    'utf8': '✓',
    'identity': 'username or email',
    'password': 'secret'
}

# authenticity_tokenの取得
s = requests.Session()
r = s.get('https://qiita.com')
print(r.text)
d = pq(r.text)

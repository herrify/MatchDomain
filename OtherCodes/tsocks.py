#!/usr/bin/env python3
#
# @author: johnny
# created: 2016-12-23
# [sudo] pip3 install pysocks
#
# http and socks5 proxy test requests
#

import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch",
    "Accept-Language": "en-US,en;q=0.8",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "DNT": "1"
}
#proxies = {"http": "http://127.0.0.1:1234", "https": "http://127.0.0.1:1234"}
proxies = {"http": "socks5://127.0.0.1:5678", "https": "socks5://127.0.0.1:5678"}
verify = False

url = 'http://httpbin.org/ip'

with requests.Session() as s:
    s.headers = headers
    s.proxies = proxies
    s.verify = verify
    r = s.get(url)
    print(r.status_code)
    if r.status_code == requests.codes.ok:
        print(r.text)



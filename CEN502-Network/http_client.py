#!/usr/bin/env python
#coding=utf-8

import urllib, urllib2

req_url = "www.google.com/cliet.py"

req_file = "cliet.py"

req = urllib2.Request(req_url)

try:
    testfile = urllib.URLopener()
    testfile.retrieve(req_url, req_file)
    urllib2.urlopen(req_url)

except: urllib2.HTTPError, e:
    print e.code
    print e.read()




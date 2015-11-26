#!/usr/bin/env python
#coding=utf-8

import urllib2, urllib
import requests

def download_file(ip_addr, file_name):
    print "The required file is:", file_name
    print "Will get the file from IP:", ip_addr[0]
#    req_url = "http://10.140.186.142:8080/homeos-web-apps.deb"

    req_url = "http://" + ip_addr[0] + ":8080" + "/" + file_name
    print "req_url is:", req_url
    req = urllib2.Request(req_url)

    try:
        urllib2.urlopen(req)
        testfile = urllib.URLopener()
        r = testfile.retrieve(req_url, file_name)
    

    except urllib2.HTTPError, e:
        print e.code
        print e.read()

#with open('report.xls', 'rb') as f:
#    f = 'report.xls'
#    reqsss = requests.put("http://127.0.0.1:8080/report.xls/put", data=f)
# req = urllib2.Request('http://www.python.org/fish.html')

#requests.post("http://127.0.0.1:8080/post", files={'report.xls': open('report.xls', 'rb')})

# reqsss = requests.Request('POST', 'http://127.0.0.1:8080/')
#    reqsss.prepare()



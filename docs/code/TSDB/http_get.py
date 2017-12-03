# -*- coding: UTF-8 -*-

import httplib, urllib
from datetime import datetime
from urllib import urlencode
from sign_sample import *
import time

# output send data
def patch_send():
    old_send= httplib.HTTPConnection.send
    def new_send( self, data ):
        print data
        return old_send(self, data) #return is not necessary, but never hurts, in case the library is changed
    httplib.HTTPConnection.send= new_send

patch_send()

# generate sign
# credentials = BceCredentials("5c5b5ea289ed4c6db75c131e7eaf5715", "ca49ed4d426541e79f7da83fde4b9e28")
credentials = BceCredentials("f73fdc86f0fa4624a7bfe9a59789378a", "2788f10a05c44c3d8ed0baa2155121bf")
http_method = "GET"
path = "/v1/metric"
headers = {"host": "zengjf.tsdb.iot.gz.baidubce.com",
    "content-type":"application/json; charset=utf-8",
    "content-length":"0"}
params = {}
timestamp = int(time.time())
result = sign(credentials, http_method, path, headers, None, timestamp)
print result
print

# send request
hdrs = {
    "Content-type": "application/json; charset=utf-8",
    "Authorization": result,
    "content-length":"0",
    "x-bce-date": '%sT%sZ' % (datetime.datetime.utcfromtimestamp(timestamp).strftime("%Y%m%d"), datetime.datetime.utcfromtimestamp(timestamp).strftime("%H%M%S"))
}
conn = httplib.HTTPConnection("zengjf.tsdb.iot.gz.baidubce.com")
conn.request("GET", "/v1/metric", headers = hdrs)
response = conn.getresponse()
print response.status, response.reason
data = response.read()
print data
conn.close()


'''
output message
>>> ================================ RESTART ================================
>>> 
bce-auth-v1/5c5b5ea289ed4c6db75c131e7eaf5715/2017-12-03T08:10:49Z/1800//3bd006b14b63da9a1dd2ab715068c6e43458203ac31e884c75d7cec953060387

GET /v1/metric HTTP/1.1

Host: zengjf.tsdb.iot.gz.baidubce.com

Accept-Encoding: identity

x-bce-date: 20171203T081049Z

content-length: 0

Content-type: application/json; charset=utf-8

Authorization: bce-auth-v1/5c5b5ea289ed4c6db75c131e7eaf5715/2017-12-03T08:10:49Z/1800//3bd006b14b63da9a1dd2ab715068c6e43458203ac31e884c75d7cec953060387




403 Forbidden
{"requestId":"b9d3e0a5-7477-4a74-942f-ea1f1e88dd6d","code":"AccessDenied","message":"Verify access forbidden"}
>>> 
'''

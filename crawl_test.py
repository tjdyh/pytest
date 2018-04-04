#!/usr/bin/python
# -*- coding: UTF-8 -*-

import urllib2
import chardet

req = urllib2.Request('http://www.zhbservice.com')
# print type(response.read())
res = urllib2.urlopen(req)
html = res.read()

char_type = chardet.detect(html)
print char_type
if char_type['encoding'].lower() != 'utf-8':
    html = unicode(html, "gbk").encode("utf-8")
fo = open("b.html", 'w')
fo.write(html)
fo.close()

# fo1 = open("b.html", 'r')
# data = fo1.read()
# print data
# fo1.close()
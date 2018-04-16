#!/usr/bin/python
# -*- coding: UTF-8 -*-

import urllib2
import chardet
import logging

#定义日志类
class Pubclilog():
    def __init__(self):
        self.logfile = './test.log'
    def iniLog(self):
        logger = logging.getLogger()
        filehandler = logging.FileHandler(self.logfile)
        streamhandler = logging.StreamHandler()
        fmt = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s')
        logger.setLevel(logging.DEBUG)
        logger.addHandler(filehandler)
        logger.addHandler(streamhandler)
        return [logger, filehandler]


#下载网页内容
def getHtml(url):
    req = urllib2.Request(url)
    # print type(response.read())
    res = urllib2.urlopen(req)
    html = res.read()
    t1 = Pubclilog()
    logger,hdlr = t1.iniLog()
    char_type = chardet.detect(html)
    logger.info(char_type)
    # print char_type
    if char_type['encoding'].lower() != 'utf-8':
        html = unicode(html, "gbk").encode("utf-8")
    fo = open("b.html", 'w')
    fo.write(html)
    fo.close()

    fo1 = open("b.html", 'r')
    data = fo1.read()
    logger.info(data)
    # print datan
    fo1.close()

if __name__ == '__main__':
    url = 'http://www.zhbservice.com'
    getHtml(url)
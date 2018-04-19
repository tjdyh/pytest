#/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib2
import urllib
import time
import ssl
import os
import threading
import logging
import random

i = 1

#解决访问https时不受信任ssl证书问题
ssl._create_default_https_context = ssl._create_unverified_context

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

#获取目标url的html内容
def getHtml(url):
    headers = [
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
        "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)"
    ]
    random_header = random.choice(headers)
    print random_header
    req = urllib2.Request(url)
    req.add_header("User-Agent", random_header)
    try:
        html = urllib2.urlopen(req)
        print "已捕获", url, "目标站数据，返回状态码为：", html.getcode()
        return html
    except urllib2.URLError,e:
        calback = e.reason
        return calback

#下载进度函数
def callBackFunc(blocknum, blocksize, totalsize):
    download_Percent = 100.0 * blocknum * blocksize / totalsize
    if download_Percent > 100:
        download_Percent = 100
    print "正在下载第 %d 张图片， 已下载 %s" % (i, download_Percent)


#生产存放图片目录
def img_dir():
    filename = "Image" + str(time.strftime("%Y-%m-%d", time.localtime()))
    if os.path.exists(filename):
        print "目录已创建"
    else:
        os.mkdir(filename)
        print "已创建目录"
        print filename

# 使用urllib模块重写下载模块
def down_img1(img_urllist):
    global i
    global j
    filename = "imge" + str(time.strftime("%Y-%m-%d", time.localtime()))
    if os.path.exists(filename):
        print "目录已创建"
    else:
        os.mkdir(filename)
        print "已创建目录"
        # print filename
    print "开始下载资源。。。"
    _path_ = os.path.abspath(filename)
    for img_url in img_urllist:
        path = os.path.join(_path_, img_url[-36:])
        print img_url
        print path
        try:
            urllib.urlretrieve(img_url, path, callBackFunc)
        except IOError, e:
            print "下载第%d张图片出现错误" % i


#多线程函数
def multiple_threads_test(img_urllist):
    #记录实验的开始时间
    t1 = time.time()
    th_lst = []
    th = threading.Thread(target=down_img1, args=[img_urllist])
    th_lst.append(th)
    for th in th_lst:
        th.start()
    for th in th_lst:
        th.join()
    #记录实验完成的时间
    t2 = time.time()
    print "使用时间：", t2-t1
    return t2-t1



if __name__ == '__main__':
    url = "http://www.zhbservice.com"
    html = getHtml(url)
    html_Doc = html.read()
    print html_Doc
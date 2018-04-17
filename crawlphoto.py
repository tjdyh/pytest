#/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib
import urllib2
import os
import time
import ssl
import threading
import logging
import random

#解决访问https时不受信任SSL证书问题
ssl._create_default_https_context = ssl._create_unverified_context

i = 1
j = 0

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


#获取源url的html内容
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
    # context = ssl._create_unverified_context()
    req = urllib2.Request(url)
    req.add_header("User-Agent",random_header)
    # req.add_header("User-Agent",send_headers)
    # html = urllib2.urlopen(req)
    # if html.getcode() == 200:
    #     # t1 = Pubclilog()
    #     # logger, hdlr = t1.iniLog()
    #     # logmsg = "已捕获%s目标站数据。。。" % url
    #     # logger.info(logmsg)
    #     print ("已捕获"),url,"目标站数据。。。"
    #     # print html.read()
    #     return html
    # else:
    #     print ("访问出现错误。。。错误代码："),html.getcode()
    #     return None
    try:
        html = urllib2.urlopen(req)
        print "已捕获", url, "目标站数据,返回状态码：", html.getcode()
        # print html.read()
        return html
    except urllib2.URLError, e:
        # print "访问出现错误，错误代码：", e.getcode()
        print e.reason
        return None

def callBackFunc(blocknum, blocksize, totalsize):
    download_Percent = 100.0 * blocknum * blocksize / totalsize
    if download_Percent > 100:
        download_Percent = 100
    print "正在下载第 %d 张图片，已下载 %s" % (i, download_Percent)

#获取子url页的图片url列表
def sub_imglist(sub_url):
    img_urllist=[]
    for sub_str in sub_url:
        img_url = sub_str["src"]
        img_urllist.append(img_url)
    print img_urllist
    return img_urllist

#生产存放图片目录
def img_dir():
    filename = "Imge" + str(time.strftime("%Y-%m-%d", time.localtime()))
    if os.path.exists(filename):
        print "目录已创建"
    else:
        os.mkdir(filename)
        print "已创建目录"
        print filename

#根据传入图片url列表依次下载图片
def down_img(img_urllist):
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
        # context = ssl._create_unverified_context()
        # f = urllib2.urlopen(img_url, context=context)
        f = urllib2.urlopen(img_url)
        data = f.read()
        with open(path, "wb") as code:
            code.write(data)

#使用urllib模块重写下载模块
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
        except IOError,e:
            print "下载第%d张图片出现错误"%i
            j += 1
        i += 1


if __name__ == '__main__':
    url = "https://www.1818df.com"
    gate_URL = url + "/pic/5/"
    print gate_URL
    html = getHtml(gate_URL)
    html_Doc = html.read()
    # print html_Doc
    threads=[]

    if html != None:
        soupHtml = BeautifulSoup(html_Doc, "lxml", from_encoding="utf-8")
        divs = soupHtml.findAll('a', target="_blank")
        print divs
        # flag = 1
        for div in divs:
            div_Doc = str(div)
            soupDiv = BeautifulSoup(div_Doc, "lxml", from_encoding="utf-8")
            htmls = soupDiv.a.get('href')
            if ".html" in htmls and "pic" in htmls:
                sub_url = url + htmls
                print sub_url
                sub_html = getHtml(sub_url)
                sub_html_Doc = sub_html.read()
                # print sub_html_Doc
                soupP  = BeautifulSoup(sub_html_Doc, "lxml", from_encoding="utf-8")
                soupP_con = soupP.find_all('img')
                # print soupP_con
                img_urllist = sub_imglist(soupP_con)
                t = threading.Thread(target=down_img1, args=[img_urllist])
                threads.append(t)
        print threads
        for t in threads:
            t.setDaemon(True)
            t.start()
            t.join()
        print "共有%d张图片下载失败！"%j
    else:
        print ("获取失败。。。")
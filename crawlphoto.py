#/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib
import urllib2
import re
import os
import time
import ssl
import threading

ssl._create_default_https_context = ssl._create_unverified_context
i = 1
#获取源url的html内容
def getHtml(url):
    send_headers = {
        'User - Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 65.0.3325.181 Safari / 537.36',
        'Accept': 'text / html, application / xhtml + xml, application / xml; q = 0.9, image / webp, image / apng, * / *;q = 0.8',
        'Connection': 'keep-alive'
    }
    # context = ssl._create_unverified_context()
    urls = urllib2.Request(url, headers=send_headers)
    # html = urllib2.urlopen(urls, context=context)
    html = urllib2.urlopen(urls)
    if html.getcode() == 200:
        print ("已捕获"),url,"目标站数据。。。"
        return html
    else:
        print ("访问出现错误。。。错误代码："),html.getcode()
        return None

def callBackFunc(blocknum,blocksize,totalsize):
    download_Percent = 100.0 * blocknum * blocksize /totalsize
    if download_Percent > 100:
        download_Percent = 100
    print "正在下载第 %d 张图片，已下载 %s" % (i, download_Percent)

#获取子url页的图片url列表
def sub_imglist(sub_url):
    img_urllist=[]
    for sub_str in sub_url:
        img_url = sub_str["src"]
        img_urllist.append(img_url)
    # print img_urllist
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
        urllib.urlretrieve(img_url, path, callBackFunc)
        i += 1


if __name__ == '__main__':
    gate_URL = "https://www.9123df.com/pic/5/"
    html = getHtml(gate_URL)
    html_Doc = html.read()
    # print html_Doc
    threads=[]

    if html != None:
        soupHtml = BeautifulSoup(html_Doc, "lxml", from_encoding="utf-8")
        divs = soupHtml.findAll('a', target="_blank")
        # print divs
        flag = 1
        for div in divs:
            div_Doc = str(div)
            soupDiv = BeautifulSoup(div_Doc, "lxml", from_encoding="utf-8")
            htmls = soupDiv.a.get('href')
            if ".html" in htmls and "pic" in htmls:
                sub_url = "https://www.9123df.com" + htmls
                # print sub_url
                sub_html = getHtml(sub_url)
                sub_html_Doc = sub_html.read()
                # print sub_html_Doc
                soupP  = BeautifulSoup(sub_html_Doc, "lxml", from_encoding="utf-8")
                soupP_con = soupP.find_all('img')
                # print soupP_con
                img_urllist = sub_imglist(soupP_con)
                # print img_urllist
                t = threading.Thread(target=down_img1, args=[img_urllist])
                threads.append(t)
        print threads
        for t in threads:
            t.setDaemon(True)
            t.start()
            t.join()

    else:
        print ("获取失败。。。")

#-*-coding:utf8-*-

__author__ = 'ice wolf'

from wxpy import *
import re
import urllib.parse
import urllib.request
import time
import os
import random

import requests
from os.path import join, abspath
requests.utils.DEFAULT_CA_BUNDLE_PATH = join(abspath('.'), 'cacert.pem')
# 同时将python安装路径\Lib\site-packages\requests\cacert.pem复制到包含exe的目录

def getReContentOnly(htmlContent,reg):
    htmlContentRe = re.compile(reg)
    htmlContentList = re.findall(htmlContentRe,htmlContent)
    if not len(htmlContentList) == 0:
        return htmlContentList[0]
    else:
        return htmlContent

def getHtml(url):
    req_header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding':'gzip, deflate',
    'Connection':'close',
    'Host':'bbs.antiy.cn',
    'Referer':'bbs.antiy.cn' #注意如果依然不能抓取的话，这里可以设置抓取网站的host
    }
    req = urllib.request.Request(url, None, req_header)#
    resp = urllib.request.urlopen(req)
    html = resp.read().decode('gbk')
    return str(html)

def getSubUrl(html,fileo,reg):
    subHtmlre = re.compile(reg)
    subHtmlList = re.findall(subHtmlre,html)
    for subHtmlUrl in subHtmlList:
        subHtmlUrl = "http://bbs.antiy.cn/forum.php?mod=viewthread&" + subHtmlUrl  #.replace('&amp;','&')
        getText(subHtmlUrl, fileo)

def getText(urlo,fileo):
    html = getHtml(urlo)
    reg1 = r'<font size="5">([1-9]{1}.+)<br />'
    textre1 = re.compile(reg1)
    textList = re.findall(textre1,html)
    n = 1
    for textEach in textList:
        reg1 = r'<.*?>'
        textEach = re.sub(reg1,'',textEach)
        reg2 = r'[&nbsp;]*'
        textEach = re.sub(reg2,'',textEach)
        print (textEach)
        fileo.write(textEach)
        fileo.write("\n")
        n += 1
    reg2 = r'(【安天】搜集整理（来源：.+)</td></tr></table>'
    textre2 = re.compile(reg2)
    textList2 = re.findall(textre2,html)
    for textEach in textList2:
        fileo.write(str(textEach))
        fileo.write("\n")
    fileo.write(urlo)

def jianxun():
    print ("Start!")
    strY = time.strftime('%Y',time.localtime(time.time()))
    strM = time.strftime('%m',time.localtime(time.time()))
    strD = time.strftime('%d',time.localtime(time.time()))
    strYMD = strY + strM + strD
    filename = "./safety_" + strYMD
    print ("Filename :" + filename)
    target = open(filename, 'w')
    target.write("每日安全简讯(" + strYMD + ")\n")
    html = getHtml("http://bbs.antiy.cn/forum.php?mod=forumdisplay&fid=52&page=1")
    reg0 = r'(tid=[0-9]{5})&amp;extra=page%3D1\"\s{1}onclick=\"atarget\(this\)\"\s{1}class=\"s\s{1}xst\">每日安全简讯\('
    reg1 = strYMD
    reg2 = r'\)<\/a>'
    reg = reg0 + reg1 + reg2 
    getSubUrl(html, target, reg)
    target.close()
    print ("Finish!")
    target = open(filename, 'r')
    jxstr = target.read()
    target.close()
    os.system("del " + "safety_" + strYMD)
    return str(jxstr)


robot = Bot(True)
L = 1
while True:
    robot.start()
    print (time.strftime('%H:%M:%S',time.localtime(time.time())))
    strH = time.strftime('%H',time.localtime(time.time()))
    strM = time.strftime('%M',time.localtime(time.time()))
    if ((L == 1) and not (strH == "07")):
        L = 0
    if (strH =="07" and L == 0):
        L = 1
        print (time.strftime('%H:%M:%S',time.localtime(time.time())))
        print ("today's message time will coming : waiting start")
        n = random.randint(0,2)
        print ("hhh : today's n is " + str(n))
        while not n == 0:
            time.sleep(420)
            robot.start()
            n -= 1
        print (time.strftime('%H:%M:%S',time.localtime(time.time())))
        print ("today's  message will send~~~")
        task_jx = robot.groups().search('xxx群')[0]
        print (task_jx)
        task_jx.send(jianxun())
    time.sleep(420)  
    if not robot.alive:
        break







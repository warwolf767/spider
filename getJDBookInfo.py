
#-*-coding:utf8-*-

__author__ = 'ice wolf'

import re
import urllib
import urllib2
import time
import traceback

def getHtml(url,lan):
    # time.sleep(3)
    req_header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection':'close',
    'Referer':None #注意如果依然不能抓取的话，这里可以设置抓取网站的host
    }
    req_timeout = 3
    req = urllib2.Request(url)#,None,req_header
    resp = urllib2.urlopen(req)#,None,req_timeout
    html = ""
    if lan == "gbk":
        html = resp.read().decode('gbk').encode('utf-8')
    else:
        html = resp.read()
    resp.close()
    return html

def getReContent(htmlContent,reg):
    htmlContentRe = re.compile(reg)
    htmlContentList = re.findall(htmlContentRe,htmlContent)
    return htmlContentList

def getReContentOnly(htmlContent,reg):
    htmlContentRe = re.compile(reg)
    htmlContentList = re.findall(htmlContentRe,htmlContent)
    if not len(htmlContentList) == 0:
        return htmlContentList[0]
    else:
        return ''

def titleSub(titleContent):
    regTitle = r'(京东套装)'
    l = re.search(regTitle,titleContent)
    if not l == None:
        return 'no'
    new = ''
    regTitle = r'(<strong>.+</strong>)'
    titleContent = re.sub(regTitle,new,titleContent)
    regTitle = r'(\s?附光盘.*)）'
    titleContent = re.sub(regTitle,new,titleContent)
    regTitle = r'(（.*DVD.*）)'
    titleContent = re.sub(regTitle,new,titleContent)
    regTitle = r'(\s?（）)'
    titleContent = re.sub(regTitle,new,titleContent)
    regTitle = r'(  )'
    titleContent = re.sub(regTitle,new,titleContent)
    regTitle = r'\''
    titleContent = re.sub(regTitle,'\\\'',titleContent)
    return titleContent

def oFile(oContent,oFilename):
    target = open(oFilename,'w')
    # zp = zip(oContent1,oContent2)
    for x in oContent:
        target.write(x) # target.write(z[0] + " " + z[1])
        target.write('\n')
    target.close()    

try:
    for x in xrange(1,239):
        filename = "sqlll--" + str(x) +".sql"
        print "Filename :" + filename
        target = open(filename, 'w')
        target.write("INSERT INTO `b_book` (`title`, `author_name`, `press`, `isbn`) VALUES")
        if x % 5 == 0:
            time.sleep(7)
        url = "http://list.jd.com/list.html?cat=1713,3287,3797&page=" + str(x) + "&sort=sort_rank_asc&trans=1&JL=6_0_0#J_main"
        try:
            html = getHtml(url,"utf8")
        except Exception,e:
            print "utf-8..."
            continue        
        reg0 = r'<a target=\"_blank\" title=\"\" href=\"\/\/item\.jd\.com\/([0-9]{6,8})\.html\">'
        urlList = getReContent(html,reg0)
        urlList = list(set(urlList))
        n = 0
        for y in urlList:
            urlE = "http://item.jd.com/" + str(y) + ".html"
            try:
                htmlE = getHtml(urlE,"gbk")
            except Exception,e:
                print "gbk..."
                continue            
            regTitle0 = r'<h1>(.+)</h1>'
            title0 = getReContentOnly(htmlE,regTitle0)
            if title0 == '':
                time.sleep(5)
                continue
            title = titleSub(title0)
            if title == 'no': 
                time.sleep(5)
                continue
            regAuthor = r'<a target=\"_blank\" href=\"\/\/book\.jd\.com\/writer\/.+\.html\">(.+)<\/a>'
            regA = r'\''
            author0 = getReContentOnly(htmlE,regAuthor)
            author = re.sub(regA,'\\\'',author0)
            regPress = r'<li title=\"(.+)\" clstag=\"shangpin\|keycount\|product'
            press = getReContentOnly(htmlE,regPress)
            regISBN = r'<li title=\"[0-9]{7,13}\">ISBN：([0-9]{7,13})<\/li>'
            ISBN = getReContentOnly(htmlE,regISBN)
            if not n == 0:
                target.write(",")
            target.write("\n")
            target.write("('" + str(title) + "', '" + str(author) + "', '" + str(press) + "', '" + str(ISBN) + "')")
            if n % 5 == 0:
                time.sleep(5)
            n += 1            
    target.close()
    print "Finish!"
except Exception, e:
    f=open("log.txt",'a')  
    traceback.print_exc(file=f)  
    f.flush()  
    f.close()

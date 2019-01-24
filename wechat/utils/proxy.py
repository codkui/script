# -*- coding: utf-8 -*-
__author__ = 'changchang.cc'

from bs4 import BeautifulSoup
from urllib import request
import http.client as httplib
import threading
import sys
from imp import reload
import time as timeM
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

reload(sys)
# sys.setdefaultencoding('utf-8')

inFile = open('./proxy.txt')
outFile = open('./verified.txt', 'w')
lock = threading.Lock()

def getProxyList(targeturl="https://www.kuaidaili.com/free/inha/"):
    countNum = 0
    proxyFile = open('proxy.txt' , 'a')
    
    requestHeader = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36"}
    
    
    for page in range(1, 50):
        url = targeturl + str(page)
        #print url
        requestObj = request.Request(url, headers=requestHeader)
        html_doc = request.urlopen(requestObj).read()
    
        soup = BeautifulSoup(html_doc, "html.parser")
        #print soup
        # trs = soup.find('table', id='ip_list').find_all('tr')
        tbody = soup.find('div', id='list').find('tbody')
        trs=tbody.find_all("tr")
        for tr in trs[1:]:
            tds = tr.find_all('td')
            # print(tr.text.strip())
            #国家
            # if tds[1].find('img') is None :
            #     nation = '未知'
            #     locate = '未知'
            # else:
            #     nation =   tds[1].find('img')['alt'].strip()
            nation  =   tds[3].text.strip()
            locate  =   tds[4].text.strip()
            ip      =   tds[0].text.strip()
            port    =   tds[1].text.strip()
            anony   =   tds[5].text.strip()
            protocol=   tds[2].text.strip()
            speed   =   tds[5].text.strip()
            time    =   tds[6].text.strip()
            
            proxyFile.write('%s|%s|%s|%s|%s|%s|%s|%s\n' % (nation, ip, port, locate, anony, protocol,speed, time) )
            print ('%s=%s:%s' % (protocol, ip, port))
            countNum += 1
        timeM.sleep(1)
    proxyFile.close()
    return countNum
    
def verifyProxyList():
    '''
    验证代理的有效性
    '''
    requestHeader = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36"}
    myurl = 'http://www.baidu.com/'

    while True:
        lock.acquire()
        ll = inFile.readline().strip()
        lock.release()
        if len(ll) == 0: break
        line = ll.strip().split('|')
        # print(line)
        protocol= line[5]
        ip      = line[1]
        port    = line[2]
        
        try:
            conn = httplib.HTTPConnection(ip, port, timeout=5.0)
            conn.request(method = 'GET', url = myurl, headers = requestHeader )
            res = conn.getresponse()
            lock.acquire()
            print("+++Success:" + ip + ":" + port) 
            outFile.write(ll + "\n")
            lock.release()
        except:
            print ("---Failure:" + ip + ":" + port)
        
    
if __name__ == '__main__':
    tmp = open('proxy.txt' , 'w')
    tmp.write("")
    tmp.close()
    proxynum = getProxyList("https://www.kuaidaili.com/free/inha/")
    print (u"国内高匿：" + str(proxynum))
    proxynum = getProxyList("https://www.kuaidaili.com/free/intr/")
    print (u"国内透明：" + str(proxynum))
    # proxynum = getProxyList("http://www.xicidaili.com/wn/")
    # print (u"国外高匿：" + str(proxynum))
    # proxynum = getProxyList("http://www.xicidaili.com/wt/")
    # print (u"国外透明：" + str(proxynum))

    print (u"\n验证代理的有效性：")
    
    all_thread = []
    for i in range(30):
        t = threading.Thread(target=verifyProxyList)
        all_thread.append(t)
        t.start()
        
    for t in all_thread:
        t.join()
    
    inFile.close()
    outFile.close()
    print ("All Done.")
# -*- coding:utf-8 -*-

import requests
import sys
import threading
import Queue
import time
import re
from bs4 import BeautifulSoup

reload(sys)  
sys.setdefaultencoding('utf8')  

header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36'}

class baidu_url(threading.Thread):
    def __init__(self,queue):
        threading.Thread.__init__(self)
        self._queue = queue
    def run (self):
        while not self._queue.empty():
            url = self._queue.get_nowait()
            try :
                self.spider(url)
            except Exception ,e:
                print e
                exit
    def spider(self,url):
        response = requests.get(url,headers=header)
        soup = BeautifulSoup(str(response.content),'lxml')
        biyingurls = soup.find_all(name='a',attrs={'target':re.compile('.'),'class':None,'h':re.compile('.')})
        for biyingurl in biyingurls:
            # print baiduurl['href']
            if 'javascript:void(0)' not in biyingurl['href']:
                # r = requests.get(url=baiduurl['href'],headers=header,timeout=8)
                # if r.status_code == 200:
                #     realurl = r.url
                if 'microsoft' not in biyingurl['href']:
                    print biyingurl['href']
                    # print time.ctime().split(' ')[3]

def main(keyword):
    queue = Queue.Queue()
    for i in range(14,28,14):
        queue.put('http://cn.bing.com/search?q='+str(keyword)+'&first='+str(i))
    threads = []
    for i in range(1):
        threads.append(baidu_url(queue))
    for t in threads:
        t.start()
    for t in threads:
        t.join()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Enter:%s keyword'%sys.argv[0]
        sys.exit(-1)
    else :
        main(sys.argv[1])
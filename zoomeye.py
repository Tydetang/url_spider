# -*- coding:utf-8 -*-

import requests
import json
import sys
import threading

reload(sys)  
sys.setdefaultencoding('utf8')  

headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'
    }

def login():
    url = "https://api.zoomeye.org/user/login"

    datas = {
        'username':'xxxx',
        'password':'xxxx'
    }
    datas = json.dumps(datas)

    r = requests.post(url,data=datas,headers=headers)
    return json.loads(r.content)['access_token']

url = 'https://www.zoomeye.org/search?t=host&q='

def action(i,):
    api_url = 'https://api.zoomeye.org/host/search?query=phpmyadmin%20'+'country:越南&page='+str(i)
    headers = {'Authorization': 'JWT '+login()}
    r = requests.get(api_url,headers=headers)
    # print r.content
    datas = json.loads(r.content)['matches']
    for data in datas:
        try :
            # print data['ip']
            url='http://'+str(data['ip'])+'/phpmyadmin/'
            response = requests.get(url,headers=headers)
            if response.status_code == 200:
                print url
        except Exception ,e:
            print e
            exit

for i in range(20,30):
    t = threading.Thread(target=action,args=(i,))
    t.start()
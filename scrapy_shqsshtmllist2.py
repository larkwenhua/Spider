import requests
import random
from bs4 import BeautifulSoup
import re
import time
import json
from jsonpath import jsonpath
import pymongo
client = pymongo.MongoClient('localhost', 27017)
shqss= client['shqss']
success_html = shqss['success_html']
error_html = shqss['error_html']
success_list = shqss['success_list']
error_list = shqss['error_list']

headers = {
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie':'UM_distinctid=1661ef56f6c2a5-08d5e15a945d4a-454c092b-1fa400-1661ef56f6d179; Hm_lvt_3406180e5d656c4789c6c08b08bf68c2=1538117693; '
             'JSESSIONID=40BA51B425CA609AD37AEBE09224C380; CNZZDATA1260383977=2118449184-1538116982-%7C1538203994; '
             'Hm_lpvt_3406180e5d656c4789c6c08b08bf68c2=1538204474'
}
proxy_list = [
    'http://39.137.107.98:80',
    'http://121.8.98.196:80',
    'http://223.202.204.195:80',
]
proxy_ip = random.choice(proxy_list) # 随机获取代理ip
proxies = {'http': proxy_ip}

def get_url_one(page):
    urllist=[]                     #初始化下网址列表
    url0 = 'http://www.shclearing.com/shchapp/web/disclosureForTrsServer/search?channelId=189&start={}&limit=200'.format(str(page))  # 基础网页
    html = requests.get(url0, headers=headers, proxies=proxies)  # 基础网页请求
    a = html.text
    jsdata = json.loads(a)
    b = '$.datas..linkurl'
    urllist = jsonpath(jsdata, b)
    return urllist

def get_url_two(page):
    urllist=get_url_one(page)
    for allurl in urllist:
        try:
            proxy_ip = random.choice(proxy_list)  # 随机获取代理ip
            proxies = {'http': proxy_ip}
            html1 = requests.get(allurl, headers=headers, proxies=proxies)  #拼接网页请求
            soup1 = BeautifulSoup(html1.text, 'lxml')                       #拼接网页清晰获取
            scripts = soup1.find_all('script', attrs={'language': 'JavaScript'})  #查找网页中script标签
            res = re.compile(r'\'.*\'')                                #正则规则
            filelist = res.findall(str(scripts[0]))                    #获取所有符合的条件的列表
            FileNames = filelist[0].split(';;')                        #获取FileName列表
            DownNames = filelist[1].split(';;')                        #获取DownNames列表
            baseurl2='http://www.shclearing.com/wcm/shch/pages/client/download/download.jsp?DownName={}&FileName={}'  #基础下载网站
            filename=str(page)+'.txt'
            for i in range(len(FileNames)):
                time.sleep(2)
                try:
                    allurl2 = baseurl2.format(str(DownNames[i].replace('\'','')),str(FileNames[i].replace('\'','')[2:]))
                    with open(filename,'a') as f:
                        f.write(allurl2+'\n')
                    success_list.insert_one({'list': allurl2})
                except Exception as ftwo:
                    print(ftwo)
                    print(allurl2)
                    error_list.insert_one({'list': allurl2})
            success_html.insert_one({'html': allurl})
        except Exception as fone:
            print(fone)
            print(allurl)
            error_html.insert_one({'html': allurl})

for page in range(35801,36402,200):
    get_url_two(page)

# *-* coding:utf-8 *-*
import requests
from bs4 import BeautifulSoup
import lxml
from multiprocessing import Process, Queue
import random
import json
import time
import requests

class Proxies(object):


    """docstring for Proxies"""
    def __init__(self, page=3):
        self.proxies = []   #ip列表
        self.verify_pro = []
        self.page = page
        self.headers = {
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8'
        }
        self.get_proxies()
        #self.get_proxies_nn()

    def get_proxies(self):

        url = 'http://www.data5u.com'
        html = requests.get(url, headers=self.headers).content
        soup = BeautifulSoup(html, 'lxml')

        uls = soup.find_all('ul', attrs={'class': 'l2'})
        ip_list1 = []
        ip_list2 = []
        ip_list3 = []
        dict1 = {'A': '0', 'B': '1', 'C': '2', 'D': '3', 'E': '4', 'F': '5', 'G': '6', 'H': '7', 'I': '8', 'Z': '9'}
        for ul in uls:
            spans = ul.find_all('span')
            if len(spans) > 3:
                ip_list1.append(spans[0].text)
                ip_list3.append(spans[3].text)
                tmp = spans[1].find('li').get('class')[1]
                a = ''
                print(spans[1])
                for j in tmp:
                    a = a + str(dict1[j])
                ip_list2.append(str(int(int(a) / 8)))
        for i in range(len(ip_list1)):
            # self.proxies.append(ip_list3[i] + '://' + ip_list1[i])
            self.proxies.append(ip_list3[i] + '://' + ip_list1[i] + ':' + ip_list2[i])




    # def get_proxies(self):
    #     page = random.randint(1,10)
    #     page_stop = page + self.page
    #     while page < page_stop:
    #         url = 'http://www.xicidaili.com/nt/%d' % page
    #         html = requests.get(url, headers=self.headers).content
    #         soup = BeautifulSoup(html, 'lxml')
    #         ip_list = soup.find(id='ip_list')
    #         for odd in ip_list.find_all(class_='odd'):
    #             protocol = odd.find_all('td')[5].get_text().lower()+'://'
    #             self.proxies.append(protocol + ':'.join([x.get_text() for x in odd.find_all('td')[1:3]]))
    #         page += 1
    #
    # def get_proxies_nn(self):
    #     page = random.randint(1,2)
    #     page_stop = page + self.page
    #     while page < page_stop:
    #         url = 'http://www.xicidaili.com/nn/%d' % page
    #         html = requests.get(url, headers=self.headers).content
    #         soup = BeautifulSoup(html, 'lxml')
    #         ip_list = soup.find(id='ip_list')
    #         for odd in ip_list.find_all(class_='odd'):
    #             protocol = odd.find_all('td')[5].get_text().lower() + '://'
    #             self.proxies.append(protocol + ':'.join([x.get_text() for x in odd.find_all('td')[1:3]]))
    #         page += 1

    def verify_proxies(self):
        # 没验证的代理
        print(self.proxies)
        old_queue = Queue()
        # 验证后的代理
        new_queue = Queue()
        print ('verify proxy........')
        works = []
        for _ in range(15):
            works.append(Process(target=self.verify_one_proxy, args=(old_queue,new_queue)))
        for work in works:
            work.start()
        for proxy in self.proxies:
            old_queue.put(proxy)
        for work in works:
            old_queue.put(0)
        for work in works:
            work.join()
        self.proxies = []
        while 1:
            try:
                self.proxies.append(new_queue.get(timeout=1))
            except:
                break
        print ('verify_proxies done!')


    def verify_one_proxy(self, old_queue, new_queue):
        while 1:
            proxy = old_queue.get()
            if proxy == 0:break
            protocol = 'https' if 'https' in proxy else 'http'
            proxies = {protocol: proxy}
            try:
                p=requests.get('http://icanhazip.com', headers=self.headers, proxies=proxies,timeout=2)
                if p.status_code==200 and p.text[0:9] in proxy:
                # if requests.get('http://www.baidu.com', proxies=proxies, timeout=2).status_code == 200:
                    print ('success %s' % proxy)
                    new_queue.put(proxy)
            except:
                pass
                # print ('fail %s' % proxy)

    # def test_ip(self,proxy,time_out = 2):
    #     '''代理IP地址（高匿）'''
    #     proxies_new=[]
    #     for each_ip in proxy:
    #         print(each_ip)
    #         '''head 信息'''
    #         head = {
    #             'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
    #             'Connection': 'keep-alive'}
    #         '''http://icanhazip.com会返回当前的IP地址'''
    #         if 'https' in each_ip:
    #             proxy_new={'https':each_ip}
    #         else:
    #             proxy_new = {'http': each_ip}
    #         try:
    #             print(proxy_new)
    #             p = requests.get('http://icanhazip.com', headers=head, proxies=proxy_new, timeout=time_out)
    #             print(p.text[0:9])
    #             if p.text[0:9] in each_ip:
    #                 proxies_new.append(proxy_new)
    #         except:
    #             pass
    #     return proxies_new

# if __name__ == '__main__':
#     a = Proxies()
#     a.verify_proxies()
#     # print(a.proxies)
#     proxie = a.proxies
#     # proxie_new=a.test_ip(proxie)
#     # print(proxie_new)
#
#     with open('proxies.txt', 'a') as f:
#        for proxy in proxie:
#              f.write(proxy+'\n')
#




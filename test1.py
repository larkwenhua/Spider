
from bs4 import BeautifulSoup
from multiprocessing import Process, Queue
import requests

class Proxies(object):

    """docstring for Proxies"""

    def __init__(self, page=3):
        self.proxies = []
        self.right_proxy = []
        self.verify_pro = []
        self.page = page
        self.headers = {
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8'
        }
        self.get_proxies()
        # self.get_proxies_nn()

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
                # print(spans[1])
                for j in tmp:
                    a = a + str(dict1[j])
                ip_list2.append(str(int(int(a) / 8)))
        for i in range(len(ip_list1)):
            # self.proxies.append(ip_list3[i] + '://' + ip_list1[i])
            self.proxies.append(ip_list3[i] + '://' + ip_list1[i] + ':' + ip_list2[i])

    def verify_one_proxy(self):

        for proxy in self.proxies:
            if proxy == 0 : break
            protocol = 'https' if 'https' in proxy else 'http'
            proxies = {protocol: proxy}
            try:
                p=requests.get('http://icanhazip.com', headers=self.headers, proxies=proxies, timeout=0.5)
                if p.status_code == 200 and p.text[0:9] in proxy:
                # if requests.get('http://www.baidu.com', proxies=proxies, timeout=2).status_code == 200:
                    self.right_proxy.append(proxy)
                    # print('success %s' % proxy)

            except:
                pass
        return self.right_proxy

a = Proxies().get_proxies()
proxie = a.proxies
print(proxie)







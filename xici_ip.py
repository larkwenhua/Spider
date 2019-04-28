import requests
from lxml import etree
import redis
import json
# import pymysql
# import MySQLdb
from concurrent.futures import ProcessPoolExecutor
import gevent


class ProxiesXiCi(object):
    start_url = 'http://www.xicidaili.com/nn'
    headers = {
        'User-Agent':'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Maxthon;'
    }
    proxies = {
        'https':'115.215.209.103:8118'
    }
    """
    抓取西刺网站的高匿ip
    """
    def __init__(self):
        # redis
        self.db = redis.StrictRedis(host='localhost', port=6379, db=0, charset='utf-8')
        # mysql
        # self.db = MySQLdb.connect(
        #     host='localhost',
        #     user='root',
        #     password='mysql',
        #     db='miaokela',
        #     charset='utf8mb4',  # 插入中文时,必须加上这一句;
        # )
        # self.cur = self.db.cursor()
        # # process_pool
        # self.pool = ProcessPoolExecutor(3)

    @classmethod
    def get_page(cls):
        """
        发起请求,获取网页
        :return:
        """
        response = requests.get(cls.start_url, headers=cls.headers, proxies=cls.proxies)
        # print(response.text)
        return response.text

    def parse(self, res_page, num):
        """
        解析提取相关数据,获取下一页链接
        :return:
        """
        # 1.创建html对象
        html = etree.HTML(res_page)
        # 2.获取节点
        # '//*[@id="ip_list"]/tbody/tr[2]'
        el_list = html.xpath('//*[@id="ip_list"]//tr')[1:]
        data_whole_list = []
        for el in el_list:
            data_dict = {}
            tds = el.xpath('./td/text()')
            print(tds)
            data_dict['ip_'] = tds[0]
            data_dict['port_'] = tds[1]
            data_dict['suf_time'] = tds[-2]
            data_dict['test_time'] = tds[-1]
            data_dict['speed_'] = el.xpath('./td[7]/div/@title')[0]
            data_dict['connect_time'] = el.xpath('./td[8]/div/@title')[0]
            data_whole_list.append(data_dict)
        # next_page = ''
        # try:
        #     next_page = 'http://www.xicidaili.com' + html.xpath('//*[@id="body"]//a[@class="next_page"]/@href')[0]
        #     print(next_page)
        # except Exception as e:
        #     print(e)
        # 直接根据url赋予next_url
        next_page = 'http://www.xicidaili.com/nn/' + str(num)
        self.start_url = next_page
        print(self.start_url)
        return data_whole_list

    def save_data_to_redis(self, data_whole_list):
        # 1.链接redis数据库
        # 2.存入数据库
        for data_ in data_whole_list:
            # 3.转化json格式
            print(data_['ip_'])
            data_json = json.dumps(data_)
            try:
                self.db.lpush(data_['ip_'], data_json)
            except:
                pass

    # def save_data_to_mysql(self, data_whole_list):
    #     # 1.创建数据库
    #     # 2.链接数据库
    #     for i in data_whole_list:
    #         try:
    #             sql = """insert into ip_pool(ip_,port,suf_time,test_time,speed,connect_time) values('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')""".format(i["ip_"],i["port_"],i["suf_time"],i["test_time"],i["speed_"],i["connect_time"])
    #             # sql = """insert into ip_pool(ip_,port,suf_time,test_time,speed,connect_time) values (1,2,3,4,5,6)"""
    #             self.cur.execute(sql)
    #         except:
    #             pass
    #         self.db.commit()

    def save_data_to_mongodb(self, data_whole_list):
        pass

    def run(self):
        num = 1
        while self.start_url:
            # 1.获取西刺网站的相应
            # 5.1 进程池并发请求
            # res_page = self.pool.submit(self.get_page).result()
            # 5.2 gevent并发请求
            # gevent.spawn()”方法会创建一个新的greenlet协程对象，并运行它。
            res_page = gevent.spawn(self.get_page).get()
            # 5.3 装饰器实现并发

            # 2.解析url,获取对应数据
            # 3.翻页
            # '//*[@id="body"]//a[@class="next_page"]'
            num += 1
            data_whole_list = self.parse(res_page, num)
            # print(data_whole_list)
            # 4.1 将数据先存入redis
            self.save_data_to_redis(data_whole_list)
            # 4.2 将数据存入mysql|mongodb
            # self.save_data_to_mysql(data_whole_list)
        # self.db.close()

if __name__ == '__main__':
    proxies_xici = ProxiesXiCi()
    proxies_xici.run()
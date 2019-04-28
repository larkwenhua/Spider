# -*- coding: utf-8 -*-
import execjs
import requests
import scrapy
import re
from WenShu.items import WenshuItem


class WenshuSpider(scrapy.Spider):
    #爬虫名、限制域名、起始链接
    name = 'wenshu'
    allowed_domains = ['gov.cn']
    start_urls = ['http://gov.cn/']
    #请求头信息
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Content-Length": "279",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Host": "wenshu.court.gov.cn",
        # "Origin": "http://wenshu.court.gov.cn",
        # "Referer": "http://wenshu.court.gov.cn/list/list/?sorttype=1&number=&guid=690f1e5d-fc1b-c74024a3-b1c2ed7f4032&conditions=searchWord+QWJS+++%E5%85%A8%E6%96%87%E6%A3%80%E7%B4%A2:%E5%A4%A7%E8%BF%9E%20%E4%B8%9C%E8%BD%AF",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0",
        "X-Requested-With": "XMLHttpRequest"
    }
    def start_requests(self):
        url = 'http://wenshu.court.gov.cn/list/list/'
        # yield发送请求，返回数据交给callback函数处理
        yield scrapy.Request(url, callback=self.parse)
    # 从请求头信息分离出cookie
    def parse(self, response):
        print(response.headers)

        cookies = str(response.headers["Set-Cookie"]).replace("b'", "")

        print('传进来的cooks : ' + cookies)
        res = re.compile(r'wzws_cid=[a-zA-Z0-9]+;')
        cookie = res.findall(cookies)[0][9:].split(';')[0]
        print('*'*50)
        print(cookie)
        # 新增代码
        # vjkl5 = getvjkl5(cookie)
        # print("vjkl5%s:" % vjkl5)

        # 调用js,通过cookie得到vl5x参数值。
        with open('getKey.js') as f:
            js = f.read()
            ctx = execjs.compile(js)
            vl5x = ctx.call('getKey', cookie)
            print('*' * 50)
            print('vl5x :%s ' % vl5x)
            a = execjs.get().name
            print(a)
            print('^' * 50)
        # 获取各参数值，函数方法写在底部
        number_1 = self.get_number()
        print("+"*50)
        number = number_1[0:4]
        print('number:%s' % number)
        guid = self.get_guid()
        print("guid:%s" % guid)
        print('*' * 50)

        # 添加获取到的cookie到headers,  cookie必须与vl5x相对应。
        self.headers['Cookie'] = cookies
        # print(self.headers)
        # 待查列表
        search_list = [
            # "天津万盛恒海金属制品有限公司",
            # "天津北方报业印务股份有限公司",
            # "中国人寿保险股份有限公司天津市分公司",
            # "天津市潮南工贸发展有限公司",
            # "中肯进出口公司",
            # "天津市津南商贸公司",
            # "天津威斯汀果汁有限公司",
            # "天津市信访办公室",
            # "天津兰德壹佰房地产投资公司",
            # "天津市津澳乳胶有限公司",
            "天津融氏乳业有限公司",
            # "富晨迎客公司",
            # "天津爱信畜禽饲料厂",
            # "天津市福港棉业有限公司",
            # "天津市红花世家油脂有限公司",
            # "天津农垦集团有限公司（机关）",
            # "天津市益源钢板有限公司",
        ]
        # 循环待查列表
        for search_name in search_list:
            # post数据
            payload = {
                'Param': '全文检索:%s' % search_name,
                       # 'Index': '1',
                       # 'Page': '10',
                       # 'Order': '法院层级',
                       # 'Direction': 'asc',
                       'vl5x': vl5x,
                       'number': number,
                       'guid': guid
            }
            res = requests.post("http://wenshu.court.gov.cn/List/ListContent", data=payload, headers=self.headers,)
            print("-" * 40)
            print(res.text)
            print("-" * 40)
            # 调用网友接口
            return_str = requests.post('http://www.ulaw.top:5677/crack', data={'a': res.text}, timeout=20).text
            print(return_str)
            # return_list =eval(return_str)
            # infos = return_str.encode('utf-8').decode('unicode_escape').replace("[[", "").replace("]]", "").split("u")
            # print(return_list)

            type = []
            date = []
            name = []
            doc_id = []
            judge_pro = []
            id = []
            court_name = []
            main_info = []

            # for infos in return_list:
            #     for info in eval(infos):
            #     print(infos)
            #         print(info)
            print("k" * 50)
            # info_number = int(len(infos)/7) - 1
            # print(info_number)
            # for i in range(0, info_number):
            #     type.append(infos[i*7+1].replace("'", "").replace(",", ""))
            #     date.append(infos[i*7+2].replace("'", "").replace(",", ""))
            #     name.append(infos[i*7+3].split("'")[1])
            #     doc_id.append(infos[i*7+3].split("'")[-2])
            #     judge_pro.append(infos[i*7+4].replace("'", "").replace(",", ""))
            #     id.append(infos[i*7+5].replace("'", "").replace(",", ""))
            #     court_name.append(infos[i*7+6].replace("'", "").replace(",", ""))
            #     main_info.append(infos[i*7+7].replace("'", ""))
            # print(data)
            # print(name_id)

            item = WenshuItem()
            item["type"] = type
            item["date"] = date
            item["name"] = name
            item["doc_id"] = doc_id
            item["judge_pro"] = judge_pro
            item["id"] = id
            item["court_name"] = court_name
            item["main_info"] = main_info
            # 将解析好的数据提交到管道文件
            print(item)






    #取得guid的值
    def get_guid(self, ):
        ctx = execjs.compile("""
                var createGuid = function () {
                return (((1 + Math.random()) * 0x10000) | 0).toString(16).substring(1);
                }
                function guid(){
                    return createGuid() + createGuid() + "-" + createGuid() + "-" + createGuid() + createGuid() + "-" + createGuid() + createGuid() + createGuid();;
                }
        """)
        fun = ctx.call("guid")
        return fun
    #取得 number
    def get_number(self):
        guid =self.get_guid()
        url = 'http://wenshu.court.gov.cn/ValiCode/GetCode'
        data = {'guid': guid}
        number = requests.post(url, headers=self.headers, data=data).text
        # print(url)
        return number



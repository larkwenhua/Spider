import requests
import random
import execjs
import re
import time
from lxml import etree

from bs4 import BeautifulSoup

import util
import json



headers = {'Host': 'www.gsxt.gov.cn',
           'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; vivo Y28L Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36 Html5Plus/1.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
           'Accept-Encoding': 'gzip, deflate',
           'Referer': 'http://www.gsxt.gov.cn/SearchItemCaptcha',
           'Connection': 'keep-alive',
           'Upgrade-Insecure-Requests': '1',
           'Cache-Control': 'max-age=0, no-cache',
           }

proxy_list = [
'http://77.85.169.149'
]
proxy_ip = random.choice(proxy_list) # 随机获取代理ip
proxies = {'http': proxy_ip}

class spider():
    session = requests.session()
    # 设置请求信息
    session.proxies = proxies
    session.headers = headers

    JSRUNTIME = execjs.get(execjs.runtime_names.Node)
    USERRESPONSE_JSCONTEXT = JSRUNTIME.compile(util.USERRESPONSE_JS)

    def get_challenge(self):

        print("getGTChallenge start")
        loginurl = "http://www.gsxt.gov.cn/SearchItemCaptcha"
        result = self.session.get(loginurl)
        if "y.replace(" not in result.text:
            raise Exception("被屏蔽了")
        mycookies = result.cookies
        # print(mycookies)
        get_js = re.findall(r'<script>(.*?)</script>', result.text)[0].replace('eval', 'return')
        resHtml = "function getClearance(){" + get_js + "};"
        # print(resHtml)
        # print("==============")
        ctx = execjs.compile(resHtml)
        # # 一级解密结果
        temp1 = ctx.call('getClearance')
        # print(temp1)
        # #
        s = 'var a' + temp1.split('document.cookie')[1].split("Path=/;'")[0] + "Path=/;';return a;"
        s = re.sub(r'document.create.*?firstChild.href', '"{}"'.format(loginurl), s)
        # print(s)
        resHtml = "function getClearance(){var window={};" + s + "};"
        ctx = execjs.compile(resHtml)
        # 二级解密结果
        jsl_clearance = ctx.call('getClearance').split(';')[0]
        # print(jsl_clearance)
        self.session.cookies['__jsl_clearance'] = str(jsl_clearance).split("=")[-1]
        results = self.session.get(loginurl).text
        print(results)
        challengeJson = json.loads(results)
        print(challengeJson)
        print("*" * 50)
        return challengeJson
    # ///////////////////////////////////////////////////
    def get_location(self):
        print("getImageGif start")
        url = "http://www.gsxt.gov.cn/corp-query-custom-geetest-image.gif?v="
        localTime = time.localtime(time.time())
        url = url + str(localTime.tm_min + localTime.tm_sec)
        print(url)
        resp = self.session.get(url).text
        script = "function dd(){var json=" + resp + ";return json.map( function(item){ return String.fromCharCode(item);}).join('');}" +"var ggg=dd();"
        # print(script)
        ctx = execjs.compile(script)
        aaa = ctx.call('dd')
        # print(aaa)
        matchObj = re.search('location_info = (\d+);', aaa)
        print("location = %s" % matchObj.group(1))
        print("*" * 50)
        return matchObj.group(1)
        # if matchObj:
        #     return matchObj.group(1)
        #     # print("aaaaaaaaa%s" % matchObj.group(0))
        # else:
        #     Exception("没有找到location_info")

    def get_token(self, location_info):
        print("get_token start")
        url = "http://www.gsxt.gov.cn/corp-query-geetest-validate-input.html?token=" + location_info

        resp = self.session.get(url).text
        js = "function dd(){var json=" + resp + ";return json.map( function(item){ return String.fromCharCode(item);}).join('');}" + "var ggg=dd();"
        ctx = execjs.compile(js)
        aaa = ctx.call('dd')
        matchObj = re.search('value: (\d+)}', aaa)
        # print(matchObj)
        if matchObj:
            location_info = matchObj.group(1)
            token = int(location_info) ^ 536870911;
            print("token=", token)
            print("*" * 50)
            return str(token)
        else:
            Exception("没有找到location_info")



    def calc_userresponse(self,distance, challenge):
        '''根据滑动距离distance和challenge，计算userresponse值'''
        # print(self.USERRESPONSE_JSCONTEXT)
        return self.USERRESPONSE_JSCONTEXT.call('userresponse', distance, challenge)

    def get_validate(self,challenge):
        '''计算validate值'''
        _r = random.randint(0, len(util.OFFLINE_SAMPLE) - 1)
        distance, rand0, rand1 = util.OFFLINE_SAMPLE[_r]
        distance_r = self.USERRESPONSE_JSCONTEXT.call('userresponse', distance, challenge)
        rand0_r = self.calc_userresponse(rand0, challenge)
        rand1_r = self.calc_userresponse(rand1, challenge)
        validate = distance_r + '_' + rand0_r + '_' + rand1_r
        print(validate)
        print("#"*60)
        return validate



    def querySearch(self, challengeJson, token, keyword):
        print("querySearch start")
        posturl = "http://www.gsxt.gov.cn/corp-query-search-1.html"
        validate = self.get_validate(challengeJson['challenge'])

        postData = {
            'tab': 'ent_tab',
            'province': '',
            'geetest_challenge': challengeJson['challenge'],
            'geetest_validate': validate,
            'geetest_seccode': validate + '|jordan',
            'token': token,
            'searchword': keyword
        }
        resp = self.session.post(posturl, postData)
        return resp.text, postData


    def dealPageUrl(self, html):
        print("dealPageUrl start")
        soup = BeautifulSoup(html, "html.parser")
        urlsItem = soup.find_all("a", class_="search_list_item db")
        pageNums = 0
        for urlItem in urlsItem:
            print("urlItem['href']=", urlItem['href'])
            # 解析页面
            url_info = "http://www.gsxt.gov.cn" + urlItem['href']
            response = self.session.get(url_info)
            print(url_info)
            html = etree.HTML(response.text)
            c = html.xpath("//dl/dt/text()|//dl/dd/text()")
            with open(r"d:/gsxx.text", 'w', encoding='utf-8') as f:
                for i in c:
                    print(i)
                    f.write(str(i) + "\n")
            f.close()
            print("%"*60)



        if len(urlsItem) > 1:
            pageForm = soup.find_all(id="pageForm")
            tabAs = pageForm[0].find_all("a", text=re.compile("\d+"))
            pageNums = len(tabAs)
        return pageNums

    def dealPageUrlNum(self, pageNums, postData):
        print("dealPageUrlNum start")
        url = "http://www.gsxt.gov.cn/corp-query-search-advancetest.html"
        for i in range(pageNums):
            postData['page'] = i + 1
            resp = self.session.get(url, params=postData)
            soup = BeautifulSoup(resp.text)
            urlsItem = soup.find_all("a", class_="search_list_item db")
            for urlItem in urlsItem:
                print("urlItem['href']=", urlItem['href'])
                # 解析页面
                url_info = "http://www.gsxt.gov.cn" + urlItem['href']
                response = self.session.get(url_info)
                print(url_info)
                html = etree.HTML(response.text)
                c = html.xpath("//dl/dt/text()|//dl/dd/text()")
                with open(r"d:/gsxx.text", 'w', encoding='utf-8') as f:
                    for i in c:
                        print(i)
                        f.write(str(i) + "\n")
                f.close()


                # for i in infos:
                #     a = 1
                #     # print(type(i))
                #     info = i.xpath("/dl[a]/dt/text()") + i.xpath("/dl[a]/dd/text()")
                #     a += 1
                #     print(info)



    def __init__(self, keyword):
        self.keyword = keyword

    # //////////////////////////////////////////////////////
    def run(self):
        # a = spider()
        challengeJson = self.get_challenge()
        print(challengeJson['challenge'])
        location = self.get_location()
        token = self.get_token(str(location))
        html, postData = self.querySearch(challengeJson, token, self.keyword)
        # print(html)
        pageNums = self.dealPageUrl(html)
        print('pageNums=', pageNums)
        # 处理多页数据
        # self.dealPageUrlNum(pageNums, postData)


a = spider("安徽经邦")
a.run()


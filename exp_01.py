import execjs
import requests
import random
import re
headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Content-Length": "279",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    # "Cookie": "_gscu_2116842793=41135640phdcng34; Hm_lvt_d2caefee2de09b8a6ea438d74fd98db2=1541135641,1541396566; _gscbrs_2116842793=1; Hm_lpvt_d2caefee2de09b8a6ea438d74fd98db2=1541396619; _gscs_2116842793=41396565dvdto718|pv:2; vjkl5=2b296e4599ff73e27b010f18542ec22e3e70968c",
    "Host": "wenshu.court.gov.cn",
    # "Origin": "http://wenshu.court.gov.cn",
    # "Referer": "http://wenshu.court.gov.cn/list/list/?sorttype=1&number=&guid=690f1e5d-fc1b-c74024a3-b1c2ed7f4032&conditions=searchWord+QWJS+++%E5%85%A8%E6%96%87%E6%A3%80%E7%B4%A2:%E5%A4%A7%E8%BF%9E%20%E4%B8%9C%E8%BD%AF",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0",
    "X-Requested-With": "XMLHttpRequest"
}
proxy_list = [
    # 'http://103.218.240.182',
    # 'http://39.137.2.198',
    'http://101.231.104.82:80',
    # 'http://211.24.103.228',
]
proxy_ip = random.choice(proxy_list) # 随机获取代理ip
# proxies = {'http': proxy_ip}
postdict={}
def get_guid():
    ctx = execjs.compile("""
            var createGuid = function () {
            return (((1 + Math.random()) * 0x10000) | 0).toString(16).substring(1);
            }
            function aa(){
                return createGuid() + createGuid() + "-" + createGuid() + "-" + createGuid() + createGuid() + "-" + createGuid() + createGuid() + createGuid();;
            }
    """)
    func = ctx.call("aa")
    return func


def get_number():
    guid = get_guid()
    url = 'http://wenshu.court.gov.cn/ValiCode/GetCode'
    data = {'guid': guid}
    res = requests.post(url, headers=headers, data=data)
    return res.text.strip()

# 获取Cookie
def get_vjkl5():
    url='http://wenshu.court.gov.cn/list/list'
    headersa={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0",
    }
    res = requests.get(url,headers=headersa)
    # print(res.headers)
    return res.headers['Set-Cookie']
# a=get_guid()
# b=get_number()
#
# d=get_vjkl5(b,a,)
# res=re.compile(r'vjkl5=[a-zA-Z0-9]+;')
# e=res.findall(d)[0]
#
# print(e)



def getvlx5(cookies):

    print('传进来的cook:'+cookies)
    res = re.compile(r'wzws_cid=[a-zA-Z0-9]+;')
    jkl5 = res.findall(cookies)[0][9:].split(';')[0]
    print(jkl5)
    print("000000000000000000000000")
    with open('getKey.js') as fp:
        js = fp.read()
        ctx = execjs.compile(js)
        vl5x = ctx.call("getKey", jkl5)
        return vl5x


def postUrl():
    guid = get_guid()
    print(guid)
    number = get_number()[0:4]
    print(number)
    vjkl5=get_vjkl5()
    cookies=vjkl5.split(';')[0]
    print(cookies)
    vl5x = getvlx5(vjkl5)
    print(vl5x)

    headers['Cookie']=cookies
    payload = {'Param': '关键词:利dad', 'Index': '1','Page': '10', 'Order': '法院层级','Direction': 'asc', 'vl5x': vl5x,'number':number, 'guid': guid}
    res=requests.post("http://wenshu.court.gov.cn/List/ListContent",data=payload,headers=headers)
                      # ,proxies=proxies)
    #
    # payload = {'Param': '全文检索:sun', 'vl5x': vl5x, 'number': number, 'guid': guid}
    # res = requests.post("http://wenshu.court.gov.cn/List/TreeContent", data=payload, headers=headers)
    # , proxies=proxies)
    print(res.text)
    return_str = requests.post('http://www.ulaw.top:5677/crack', data={'a': res.text}, timeout=20).text
    print(return_str)
postUrl()
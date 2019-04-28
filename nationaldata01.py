import requests
import json
import time
import os
import threading
import multiprocessing
from selenium import webdriver

# browser = webdriver.Chrome()
path = 'D:\国家数据'

# option = webdriver.ChromeOptions()
# option.add_extension(r'D:\Downloads\set-character-encoding-0.50.crx')  # 自己下载的crx路径
# option.add_argument('UTF-8')
# browser = webdriver.Chrome(chrome_options=option)
# urltest = 'http://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=hgyd&rowcode=zb&colcode=sj&wds=%5B%5D&dfwds=%5B%7B%22wdcode%22%3A%22zb%22%2C%22valuecode%22%3A%22A010C0A%22%7D%5D&k1=1555911886161'
# browser.get(urltest)
# time.sleep(10)
if not os.path.exists(path):
    os.makedirs(path)

class gjsj():
    # code_list = ['A01', 'A02','A03', 'A04', 'A05', 'A06']
    # code_list = ['A01', 'A02',]
    info_list = []
    t = time.time()
    timestamp = int(round(t * 1000))
    # 获取编码
    def prase_code(self, code_list):
        # print(code_list)
        for code in code_list:

            path_root = path + os.path.sep + code
            if not os.path.exists(path_root):
                os.makedirs(path_root)
        print('-----1------')

        for code in code_list:
            # 根据code创建大类文件夹
            # print(code)
            # 月度数据
            # url = 'http://data.stats.gov.cn/easyquery.htm?id={}&m=getTree&dbcode=hgyd&wdcode=zb'.format(code)
            # 季度数据
            # url = 'http://data.stats.gov.cn/easyquery.htm?id={}&m=getTree&dbcode=hgjd&wdcode=zb'.format(code)
            # 年度数据
            url = 'http://data.stats.gov.cn/easyquery.htm?id={}&m=getTree&dbcode=hgnd&wdcode=zb'.format(code)
            response = requests.get(url).text

            # browser.get(url)
            # time.sleep(1)
            # response = browser.find_element_by_xpath("//body").text
            # print(response)
            list_info = json.loads(response)
            for info in list_info:
                # {"dbcode": "hgyd", "id": "A0209", "isParent": true, "name": "工业主要产品产量", "pid": "A02", "wdcode": "zb"},
                # {"dbcode": "hgyd", "id": "A020A", "isParent": false, "name": "工业企业主要经济指标", "pid": "A02", "wdcode": "zb"}
                # 有子节点，根据id创建文件夹
                if info['isParent'] == True:
                    code_list.append(info['id'])
                    path_name = path + os.path.sep + info['pid'] + os.path.sep + (info['id'] + '--' + info['name'])
                    if not os.path.exists(path_name):
                        os.makedirs(path_name)
                else:
                # 无子节点，将信息添加到列表中
                    infos = info['id'] + '--' + info['name'] + '--' + info['pid']
                    self.info_list.append(infos)
        return self.info_list

    # 获取详细信息

    def prase_info(self, info_list):

        print('-----2------')
        for each in info_list:
            print(each)
            data_detail = []
            dcode = each.split('--')[0]
            # print(dcode)
        #     dcode = 'A0201'
            m = 'QueryData'
            dbcode = 'hgnd'
            rowcode = 'zb'
            colcode = 'sj'
            wds = '[]'
            dfwds = '[{"wdcode":"zb","valuecode":"%s"},{"wdcode":"sj","valuecode":"1949-2019"}]' % dcode
            url = 'http://data.stats.gov.cn/easyquery.htm?m={}&dbcode={}&rowcode={}&colcode={}&wds={}&dfwds={}&k1={}'.format( m, dbcode, rowcode, colcode, wds, dfwds, self.timestamp)
            response = requests.get(url).text

            # browser.get(url)
            # response = browser.find_element_by_xpath("//body").text
            mid_info = json.loads(response)
            a = mid_info['returndata']['datanodes']
            b = mid_info["returndata"]["wdnodes"][0]["nodes"]
            # print(a)
            # print(b)
            # 名称和单位 b 为列表
            dict = {}
            for i in b:
                dict2 = {i['code']: i['name'] + '_' + i['unit']}
                dict.update(dict2)
            # print(dict)
            # # 打开要写入过滤后信息的文件
            i = 0
            while i < len(a):
                # 时间和数据 ，a 为列表
                time = a[i]['wds'][1]['valuecode']
                code_1 = a[i]['wds'][0]['valuecode']
                data = a[i]['data']['data']
                code_name = dict[code_1]
                # 提取后的信息
                all_info = str(code_name) + '_' + str(time) + "_" + str(data)
                # print(all_info)
                data_detail.append(all_info)
                i += 1
            data_detail.insert(0, each)
            yield data_detail

    def write_info(self, data):
        print('-----3------')
        name = (data[0]).split('--')
        print(name)
        filename_dict = {}
        path_now = path + '\\' + name[-1][0:3]
        if len(name[0]) > 5:

            for dirnames in os.walk(path_now):
                dir_name = (dirnames[0].split('\\')[-1]).split('--')
                if len(dir_name) > 1:
                    dict3 = {dir_name[0]:dir_name[1]}
                    filename_dict.update(dict3)
            print(filename_dict)
            aaa = filename_dict[name[-1]]
            filename_path = path_now + os.path.sep + name[-1]+'--'+aaa + os.path.sep + data[0].replace('/','_') + '.txt'
            if not os.path.exists(filename_path):
                with open(filename_path, 'w', encoding='utf-8') as f:
                    for msg in data[1:]:
                        f.write(msg + "\n")
                    f.close()
            else:
                print('文件已存在！！！')
        else:
            filename_path1 = path_now + os.path.sep + data[0].replace('/','_') + '.txt'
            if not os.path.exists(filename_path1):
                with open(filename_path1, 'w', encoding='utf-8') as f:
                    for msg in data[1:]:
                        f.write(msg + "\n")
                    f.close()
            else:
                print('文件已存在！！！')

    def main(self):

        list = [ 'A0201']

        a = self.prase_code(list)
        print(a)
        b = self.prase_info(a)
        for i in b:

            print(i)
            self.write_info(i)
    def threads(self):
        # 多线程实例化
        threads = []
        t = gjsj()
        # 线程数
        for ii in range(2):
            print('线程编号：%s' % ii)
            t1 = threading.Thread(target=t.main)
            # 延时启动线程，排除创建文件夹错误
            time.sleep(1)
            t1.start()
            threads.append(t1)
if __name__ == '__main__':
    q = gjsj()
    q.main()
    # pool = multiprocessing.Pool(processes=3)
    # for i in range(1, 5):
    #     print('进程编号：%s' %i)
    #     pool.apply_async(func=q.main())
    # pool.close()
    # pool.join()  #在join之前一定要调用close，否则报错
    # print("执行完毕！")

# -*- coding: utf-8 -*-
import scrapy
import os
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from THS_02.items import Ths02Item
from scrapy.http import Request
from THS_02.items import Ths02Item

curPath = './date'
class ThsSpider(CrawlSpider):
    name = 'ths'
    allowed_domains = ['q.10jqka.com.cn', 'stockpage.10jqka.com.cn']
    start_urls = [
                    # 'http://q.10jqka.com.cn/thshy',
                    'http://q.10jqka.com.cn/thshy/detail/code/881131/',
                  ]

    industry_re = LinkExtractor(allow=r'(http|https):\/\/\w\.[0-9a-zA-Z.]+/\D+/\d+.(?!.*%)')
    company_re = LinkExtractor(allow=r'(http|https):\/\/\w.[\D+]+\d+\D+\d+/$')


    # company_re = LinkExtractor(restrict_xpaths='html/body/div[2]/div[2]/div[3]/table/tbody/tr/td[2]')
    rules = (
        Rule(industry_re, callback='parse_industry', follow=True),
        Rule(company_re, callback='parse_company', follow=True),
    )
    j = 0
    i = 0
    item = Ths02Item()
    def parse_industry(self, response):
        pass
        # if len(response.url) < 50:
        #     print("行业%d：%s" % (self.i, response.url))
        #     # 将获取到的行业链接添加到起始URL列表中
        #     self.start_urls.append(response.url)
        #     for each in response.xpath('//div[2]/div[2]/div[1]/h2').extract():
        #         # 手动延时
        #         # time.sleep(1)
        #         # 行业信息
        #         industry_info1 = each.replace('简介</h2>', ':')
        #         industry_info2 = industry_info1.replace('<h2>', '')
        #         # print(industry_info1)
        #         industry_info2 = industry_info2 + response.url
        #         industry_number = industry_info2.split('/')[-2]
        #         print(industry_info2)
        #         self.item['industry_info'] = industry_info2
        #         self.item['industry_number'] = industry_number
        #     self.i += 1
        #
        # print("***** %d *******" % self.i)

    def parse_company(self, response):
        # print(response.text)
        url = response.url
        print("公司：%s" % url)
        # self.j += 1
        # for each in response.xpath('//h1/a[1]/strong').extract():
        #     # 手动延时
        #     # time.sleep(1)
        #     # print(each)
        #     company_info1 = each.replace('<strong>', '')
        #     company_info2 = company_info1.replace('</strong>', ':') + url
        #     company_number = company_info2.split('/')[3]
        #     # print(company_info2)
        #     self.item['company_info'] = company_info2
        #     self.item['company_number'] = company_number

            # tempPath = company_number
            # print(tempPath)
            # targetPath = curPath + os.path.sep + tempPath
            # if not os.path.exists(targetPath):
            #     os.makedirs(targetPath)

        print("------- %d -------" % self.j)


        yield self.item




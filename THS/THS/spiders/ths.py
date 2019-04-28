# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from THS.items import ThsItem
import time
import requests
import demjson
class ThsSpider(CrawlSpider):
    name = 'ths'
    allowed_domains = ['q.10jqka.com.cn', 'stockpage.10jqka.com.cn']
    start_urls = ['http://q.10jqka.com.cn/thshy']

    code_link = LinkExtractor(allow=r'(http|https):\/\/\w\.[0-9a-zA-Z.]+/\D+/\d+.(?!.*%)')
    rules = (
        Rule(code_link, callback='parse_code', follow=True),

    )

    def parse_code(self, response):
        #声明实体类
        item = ThsItem()
        #行业信息（URL）
        item['code_info'] = response.url
        self.start_urls.append(response.url)


        for each in response.xpath('//table/tbody/tr/td[3]').extract():
            #手动延时
            # time.sleep(1)
            industry_info1 = each[13:-9].replace('" target="_blank">', '')
            industry_info2 = industry_info1.replace('http://stockpage.10jqka.com.cn/', ' ')
            # print(industry_info2)
            #行业下子公司信息（编码+名称）
            item["industry_info"] = industry_info2

            #行业下子公司编码（编码）
            industry_number = industry_info2[1:7]
            item['industry_number'] = industry_number


            yield item












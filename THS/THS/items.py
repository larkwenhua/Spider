# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ThsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #行业信息
    code_info = scrapy.Field()

    # 公司信息
    industry_info = scrapy.Field()
    industry_number = scrapy.Field()

    #数据类型
    data_cash = scrapy.Field()
    data_benefit = scrapy.Field()
    data_debt = scrapy.Field()
    data_main = scrapy.Field()
    #数据期数
    simple_data = scrapy.Field()
    report_data = scrapy.Field()
    year_data = scrapy.Field()






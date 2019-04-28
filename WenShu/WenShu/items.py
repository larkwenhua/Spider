# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WenshuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 实例化对象
    # 案件类型’,‘裁判日期’,‘案件名称’,‘文书ID’,‘审判程序’,‘案号’,‘法院名称’,‘裁判要旨
    type = scrapy.Field()
    date = scrapy.Field()
    name = scrapy.Field()
    doc_id = scrapy.Field()

    judge_pro = scrapy.Field()
    id = scrapy.Field()
    court_name = scrapy.Field()
    main_info = scrapy.Field()


# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Ths02Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    industry_info = scrapy.Field()
    industry_number = scrapy.Field()
    company_info = scrapy.Field()
    company_number = scrapy.Field()

    pass

# -*- coding: utf-8 -*-
from tianyancha import Tianyancha
# 单个
table_dict = Tianyancha(username='18242260608', password='1475433947lark').tianyancha_scraper(keyword='安徽经邦', table=['baseInfo', 'staff', 'invest'], export='xlsx')
# 批量
# tuple_dicts = Tianyancha(username='User', password='Password').tianyancha_scraper_batch(input_template='input.xlsx', export='xlsx')
# tuple_dicts[0]
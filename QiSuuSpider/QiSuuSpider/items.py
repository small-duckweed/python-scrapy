# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QisuuspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class BookItem(scrapy.Item):

    categray = scrapy.Field() # 小说分类
    star = scrapy.Field() # 等级
    detail_url = scrapy.Field() # 详情url地址
    src = scrapy.Field() # 封面图地址
    name = scrapy.Field() # 小说名称
    click_num = scrapy.Field() # 点击次数
    file_size = scrapy.Field() # 文件大小
    book_type = scrapy.Field() # 小说类型
    update_time = scrapy.Field() # 更新日期
    status = scrapy.Field() # 连载状态
    author = scrapy.Field() # 书籍作者
    run_type = scrapy.Field() # 运行环境
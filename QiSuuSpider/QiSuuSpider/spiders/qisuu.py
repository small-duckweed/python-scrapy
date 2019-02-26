# -*- coding: utf-8 -*-
import scrapy
from ..items import BookItem

class QisuuSpider(scrapy.Spider):
    name = 'qisuu'
    allowed_domains = ['qisuu.com','baidu.com']
    start_urls = ['https://www.qisuu.com/']
    # 基础地址
    base_url = 'https://www.qisuu.com'

    def parse(self, response):
        # 解析首页拿到分类地址
        links = response.xpath('//div[@class="nav"]/a')
        # for循环 遍历所有a
        # enumerate() 枚举 产生就是索引对应值
        for index,a in enumerate(links):
            # 不要第1个a标签
            if index == 0:
                continue
            categray = a.xpath('text()').extract_first('')
            href = a.xpath('@href').extract_first('')
            print(categray,href)
            # 拼接完整的分类地址
            cg_url = self.base_url + href
            # 创建请求对象,并且使用yield交给引擎处理
            # meta 是一个字典,可以用于页面解析时传递参数
            yield scrapy.Request(
                url=cg_url,
                callback=self.parse_categray,
                meta={'categray':categray}
            )
    # 解析分类页面
    def parse_categray(self, response):
        print('parse_categray调用了')
        # 根据key从response.meta中取出传递过来的分类
        # categray = response.meta.get('categray')
        # 找到当前页所有的小说信息
        lis = response.xpath('//div[@class="listBox"]/ul/li')
        for li in lis:
            star = li.xpath('div/em/@class').extract_first('')
            href = li.xpath('a/@href').extract_first('')
            # print(star,href)
            # 拼接完整的url
            detail_url = self.base_url+href
            # 向meta中添加小说等级\小说详情地址
            response.meta['star'] = star
            response.meta['detail_url'] = detail_url

            yield scrapy.Request(
                url=detail_url,
                callback=self.parse_detail,
                meta=response.meta
            )
        # 找到下一页
        # next_as = response.xpath('//div[@class="tspage"]/a')
        next_href = response.xpath('//a[contains(text(),"下一页")]/@href').extract_first('')
        if next_href:
            if '3' in next_href:
                return
            # 发起请求
            yield scrapy.Request(
                url=self.base_url + next_href,
                callback=self.parse_categray,
                # 为什么要传递meta?
                # 下一页的小说也需要分类信息,分类信息在response的meta中
                meta=response.meta
            )


        # for a in next_as:
        #     # for循环遍历每一个a标签,取出a的文本
        #     text = a.xpath('text()').extract_first('')
        #     # 如果a标签的文本不是下一页,不发起请求
        #     if '下一页' == text:
        #         href = a.xpath('@href').extract_first('')
        #         # 发起请求
        #         yield scrapy.Request(
        #             url=self.base_url+href,
        #             callback=self.parse_categray
        #         )


    # 解析小说详情页面
    def parse_detail(self, response):

        # 从meta中取出分类\等级\地址
        categray = response.meta.get('categray')
        star = response.meta.get('star')
        # 取等级数字
        star = star[-1]
        detail_url = response.meta.get('detail_url')
        # 封面图
        src = response.xpath('//div[@class="detail_pic"]/img/@src').extract_first('')
        src = self.base_url+src
        # 小说名称
        name = response.xpath('//div[@class="detail_right"]/h1/text()').extract_first('')
        # 小说详细信息
        infos = response.xpath('//div[@class="detail_right"]/ul/li/text()').extract()
        # 点击次数
        click_num = infos[0].split('：')[-1]
        # 文件大小
        file_size = infos[1].split('：')[-1]
        # 书籍类型
        book_type = infos[2].split('：')[-1]
        # 更新日期
        update_time = infos[3].split('：')[-1]
        # 连载状态
        status = infos[4].split('：')[-1]
        # 书籍作者
        author = infos[5].split('：')[-1]
        # 运行环境
        run_type = infos[6].split('：')[-1]

        # yield item 交给pipeline处理
        item = BookItem()
        item['run_type'] = run_type
        item['author'] = author
        item['status'] = status
        item['update_time'] = update_time
        item['book_type'] = book_type
        item['file_size'] = file_size
        item['click_num'] = click_num
        item['name'] = name
        # 下载图片,该属性必须是一个列表
        item['src'] = [src]
        # 把网页文件下载到本地,该属性必须是一个列表
        item['detail_url'] = [detail_url]
        item['star'] = star
        item['categray'] = categray
        yield item









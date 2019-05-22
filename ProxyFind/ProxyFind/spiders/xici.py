# -*- coding: utf-8 -*-
import scrapy
import requests
from ProxyFind.items import ProxyfindItem

class XiciSpider(scrapy.Spider):
    name = 'xici'
    allowed_domains = ['xicidaili.com']
    start_urls = []
    for i in range(1,2):
        start_urls.append('https://www.xicidaili.com/nn/' + str(i))

    def parse(self, response):
        ip = response.xpath('//tr[@class]/td[2]/text()').extract()
        port = response.xpath('//tr[@class]/td[3]/text()').extract()
        agreement_type = response.xpath('//tr[@class]/td[6]/text()').extract()
        proxies = zip(ip, port, agreement_type)
        print('proxies',proxies)
        # 代理是否可用
        for ip, port, agreement_type in proxies:
            proxy = {
                'http':agreement_type.lower() + '://' + ip + ':' + port,
                'https:':agreement_type.lower() + '://' + ip + ':' + port
            }
            try:
                print('proxy = ', proxy)
                res = requests.get('https://www.baidu.com/', proxies=proxy, timeout=2)
                print(res.status_code)
                if res.status_code == 200:
                    print('success %s' % ip)
                    item = ProxyfindItem()
                    item['proxy'] = proxy
                    print('--------------------------------------------------')
                    yield item
            except:
                print('fail %s' % ip)

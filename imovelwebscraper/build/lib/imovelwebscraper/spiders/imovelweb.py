# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.spiders import CrawlSpider, Rule
#from urllib.parse import urljoin
import re
from selectorlib import Extractor

class ImovelwebSpider(scrapy.Spider):
    name = 'imovelweb'
    allowed_domains = ['https://www.imovelweb.com.br/']
    start_urls = ['https://www.imovelweb.com.br/apartamentos-aluguel-sao-paulo-sp.html']
    state = True
    download_delay = 2
    def parse(self, response):
        for city in response.css('h2[class=posting-title] a::attr(href)').extract():
            yield Request(urljoin(response.url, city), callback=self.parse_arrumar,
                          dont_filter=self.state)

        next_page = response.xpath('//li[@class="pag-go-next"]/a/@href').extract_first()
        if next_page:
            print(next_page)
            yield Request(urljoin(response.url, next_page),
                          callback=self.parse,dont_filter=False
                )
    
    def find_lat_lon(self, text):
        numbers = re.findall(r"[-+]?\d*\.\d+|\d+", text)
        #print(float(numbers[0]), float(numbers[1]))
    
    def extract_from_yml(self, response):
        e = Extractor.from_yaml_file('selectors.yml')
        data = e.extract(response.text)
        if data['rent'] == None and data['sell'] != None:
            data['rent'] = data['sell']
            data['sell'] = None
        
        print(data)
        
    def parse_imovel(self, response):
        for city in response.css('h2[class=posting-title] a::attr(href)').extract():
            yield Request(response.urljoin("/"+city), callback=self.parse_arrumar,
                          dont_filter=self.state)

    def parse_arrumar(self, response):
        maps = "//div[@id='article-map']//img[@id='static-map']//img"
        text = response.xpath("//div[@id='article-map']//img").extract_first()
        self.extract_from_yml(response)
        self.find_lat_lon(text)

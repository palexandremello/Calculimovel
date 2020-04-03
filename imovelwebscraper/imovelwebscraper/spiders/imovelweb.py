import scrapy
from scrapy.http import Request
from scrapy.spiders import CrawlSpider, Rule
from urllib.parse import urljoin
import re
from selectorlib import Extractor
import unicodedata
from decimal import Decimal
from imovelwebscraper.items import ImovelwebscraperItem
from scrapy.linkextractors import LinkExtractor

class ImovelwebSpider(CrawlSpider):
    name = 'imovelweb'
    allowed_domains = ['https://www.imovelweb.com.br/']
    start_urls = ['https://www.imovelweb.com.br/apartamentos-aluguel-sao-paulo-sp.html']
    state = True
    download_delay = 1
    custom_settings = {
    'CONCURRENT_REQUESTS': 20,
    }   
             

    def __init__(self, *args, **kwargs):
        super(ImovelwebSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['https://www.imovelweb.com.br/apartamentos-aluguel-sao-paulo.html']
        
    def parse(self, response):
        for city in response.css('h2[class=posting-title] a::attr(href)').getall():
            print(city)
            #yield response.follow(urljoin(self.allowed_domains[0], city), callback=self.parse_items)
            yield Request(urljoin(self.allowed_domains[0], city), callback=self.parse_summary, dont_filter=True)
            #print(response.url)
        
        next_page = response.xpath('//li[@class="pag-go-next"]/a/@href').extract_first()
        if next_page is not None:
            print(next_page)
            yield response.follow(self.allowed_domains[0]+next_page,self.parse, dont_filter=True)
            #yield Request(urljoin(self.allowed_domains[0], next_page),
            #              callback=self.parse,dont_filter=True
            #    )

    def parse_summary(self, response):
        maps = response.xpath("//div[@id='article-map']//img").extract_first()
        numbers = re.findall(r"[-+]?\d*\.\d+|\d+", maps)

        e = Extractor.from_yaml_file('selectors.yml')
        data = e.extract(response.text)
        if data['rent'] == None and data['sell'] != None:
            data['rent'] = data['sell']
            data['sell'] = None

        if data['expenses'] != None:
            expensives = float(re.sub(r'[^\d,]', '', data['expenses'].split(' ')[1]))
            data['expenses'] = float(expensives)
        else:
            data['expenses'] = 0.0
        
        if data['sell'] != None:
            data['sell'] = float(re.sub(r'[^\d,]', '', data['sell'].split(' ')[1]))
        else:
            data['sell'] = 0.0

        if data['rent'] != None:
            data['rent'] = float(re.sub(r'[^\d,]', '', data['rent'].split(' ')[1]))
        else:
            data['rent'] = 0.0


        if data['ageImovel'] != None:
            data['ageImovel'] = int(data['ageImovel'].split(' ')[0])
        else:
            data['ageImovel'] = "NaN"
        
        print("codImovel: %s" % (data['codRealEstate'].split('Cód. Imovelweb: ')[1]))
        items = ImovelwebscraperItem(codImovel=data['codRealEstate'].split('Cód. Imovelweb: ')[1],
                lat=               float(numbers[0]),
                lon=               float(numbers[1]),
                areaTotal=         int(data['totalArea'].split('m²')[0]),
                areaUsavel=        int(data['usableArea'].split('m²')[0]),
                banheiros=        int(data['bathrooms'].split(' ')[0]),
                garagem=           int(data['garage'].split(' ')[0]),
                quartos=           int(data['bedrooms'].split(' ')[0]),
                suite=           int(data['suite'].split(' ')[0]),
                bairro=            data['addres2'].split(',')[1].strip(),
                cidade=            data['addres2'].split(',')[2].strip(),
                aluguel=           data['rent'],
                condominio=        data['expenses'],
                valorDeVenda=      data['sell'],
                idadeImovel=       data['ageImovel'])



        yield items
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ImovelwebscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    codImovel = scrapy.Field(serializer=str)
    lat = scrapy.Field()
    lon = scrapy.Field()
    areaTotal= scrapy.Field()
    areaUsavel = scrapy.Field()
    banheiros = scrapy.Field()
    garagem = scrapy.Field()
    quartos = scrapy.Field()
    suite = scrapy.Field()
    bairro = scrapy.Field(serializer=str)
    cidade = scrapy.Field(serializer=str)
    aluguel = scrapy.Field()
    condominio = scrapy.Field()
    valorDeVenda = scrapy.Field()
    idadeImovel = scrapy.Field()


# -*- coding: utf-8 -*-
from scrapy.http.response import Response
import scrapy


class WalletSpider(scrapy.Spider):
    name = 'wallet'
    start_urls = ['https://wallet.ua/c/f-laptop_bags-pol_muzhskoj/']

    def parse(self, response: Response):
        products = response.xpath("//div[contains(@class, 'prd-wrap')]")[:20]
        for product in products:
            yield {
                'description': product.xpath(".//a[@class='name']/text()").get(),
                'price': product.xpath(".//span[@class='crate']/@data-rate").get(),
                'img': "https://wallet.ua" + product.xpath(".//img[@class='first-picture']/@src").get()
            }

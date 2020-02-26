from scrapy.spiders import Spider
from scrapy import Selector
from lxml import etree
from lab1.spiders import BaseSpider


def _names(response):
    names_el = Selector(response=response) \
        .xpath(f'//*[@class="name"]')
    return [n.xpath('normalize-space(.)').get()
            for n in names_el]


def _images(response):
    return Selector(response=response) \
        .xpath(f'//*[@data-position=0]/@data-src').getall()


def _prices(response):
    return Selector(response=response) \
            .xpath(f'//*/@data-price-amount').getall()


def _descriptions(response):
    descriptions_el = Selector(response=response) \
        .xpath(f'//*[@class="attributes"]')
    return [d.xpath('normalize-space(.)').get()
            for d in descriptions_el]


class SokolSpider(BaseSpider, Spider):
    """Spider to grab goods info from sokol.ua"""

    name = 'sokol'
    start_urls = ['https://sokol.ua/products/multivarki/?product_list_limit=24']
    pages = 20

    def parse(self, response):
        names = _names(response)
        images = _images(response)
        prices = _prices(response)
        descrs = _descriptions(response)

        for n, i, p, d in zip(names, images, prices, descrs[:self.pages]):
            yield {
                'name': n, 'image': i,
                'price': p, 'description': d
            }

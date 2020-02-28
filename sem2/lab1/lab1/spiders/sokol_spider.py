from urllib.parse import urljoin
import json
from pprint import pprint
from scrapy.spiders import Spider, Request
from scrapy import Selector
from lxml import etree

from lab1.spiders import BaseSpider


class SokolSpider(BaseSpider, Spider):
    """Spider to grab goods info from sokol.ua"""

    name = 'sokol'
    start_urls = ['https://sokol.ua/products/holodilniki/?product_list_limit=24']
    pages = 20

    def parse(self, response):
        links = Selector(response=response) \
                .xpath('//a[@class="name"]/@href') \
                .getall()[:SokolSpider.pages]
        for link in links:
            yield Request(url=urljoin(response.url, link),
                          callback=self.parse_frifges)

    def parse_frifges(self, response):
        selector = Selector(response=response)
        script = selector.xpath('//script[contains(text(), "gallery/gallery")]/text()').get()
        data = json.loads(script)
        image = data['[data-gallery-role=gallery-placeholder]']['mage/gallery/gallery']['data'][0]['img']

        yield {
            'name': selector.xpath('//span[@itemprop="name"]/text()').get(),
            'price': selector.xpath('//span[@class="price-wrapper"]/@data-price-amount').get(),
            'image': image,
            'description': selector.xpath('normalize-space(//div[@class="product_prop_anons"])').get()
        }

    @staticmethod
    def create_xhtml_table():
        dom = etree.parse('output/sokol.xml')
        xslt = etree.parse('transformation.xsl')
        transform = etree.XSLT(xslt)
        new_dom = transform(dom)
        with open('output/table.xhtml', 'w') as f:
            f.write(etree.tostring(new_dom, pretty_print=True).decode())

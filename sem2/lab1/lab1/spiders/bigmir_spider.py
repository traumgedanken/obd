from lxml import etree
from scrapy import exceptions, Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from lab1.spiders import BaseSpider


class BigmirSpider(BaseSpider, CrawlSpider):
    """Spider to grab all text and images from bigmir.net"""

    name = 'bigmir'
    start_urls = ['https://www.bigmir.net/']
    pages_max = 5

    rules = [Rule(LinkExtractor(allow='bigmir.net'),
                  callback='parse_url', follow=True)]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.visited_pages = []
        self.redirected_from = dict()

    @classmethod
    @property
    def output_file(cls):
        return f'{cls.name}.'

    def _check_stop_criteria(self):
        if len(self.visited_pages) >= BigmirSpider.pages_max:
            raise exceptions.CloseSpider('Maximum visited pages number exceeded')

    def parse_url(self, response):
        self._check_stop_criteria()

        if response.url not in self.visited_pages:
            self.visited_pages.append(response.url)

            text_data = Selector(response=response) \
                .xpath('//p//text() | //a//text()').getall()
            images = Selector(response=response) \
                .xpath('//img/@src').getall()

            yield {
                'url': response.url,
                'text_data': [t.strip() for t in text_data],
                'images': [response.urljoin(src) for src in images]
            }

    @classmethod
    def analyze(cls):
        pages = etree.parse(cls.get_data_filename()) \
            .xpath('page')

        def img_count(el):
            return int(el.xpath("count(fragment[@type='image'])"))

        page = min(pages, key=img_count)
        return page.xpath('./@url')[0], img_count(page)

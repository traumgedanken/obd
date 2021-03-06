"""Module with defined pipelines for scrapy"""
from lxml import etree

from lab1.spiders import BigmirSpider, SokolSpider


def _create_sub_element(parent, tag, attrib={},
                        text=None, nsmap=None, **_extra):
    result = etree.SubElement(parent, tag, attrib, nsmap, **_extra)
    result.text = text
    return result


class XMLPipeline(object):
    """Pipeline to save items in XML file"""

    def __init__(self):
        self.data = None
        self.doc = None

    def open_spider(self, spider):
        self.data = etree.Element('data')
        self.doc = etree.ElementTree(self.data)

    def close_spider(self, spider):
        self.doc.write(spider.get_data_filename(), xml_declaration=True,
                       encoding='utf-8', pretty_print=True)

    def process_item(self, item, spider):
        if isinstance(spider, BigmirSpider):
            self._process_bigmir_item(item)
        elif isinstance(spider, SokolSpider):
            self._process_sokol_item(item)

    def _process_bigmir_item(self, item):
        page = etree.Element('page', url=item['url'])
        for text in item['text_data']:
            if text:
                _create_sub_element(page, 'fragment', type='text', text=text)
        for src in item['images']:
            _create_sub_element(page, 'fragment', type='image', text=src)
        self.data.append(page)

    def _process_sokol_item(self, item):
        good = etree.Element('good', name=item.pop('name'))
        for key, value in item.items():
            _create_sub_element(good, key, text=value)
        self.data.append(good)


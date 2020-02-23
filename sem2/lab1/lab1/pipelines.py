from lxml import etree


def _create_sub_element(parent, tag, attrib={},
                        text=None, nsmap=None, **_extra):
    result = etree.SubElement(parent, tag, attrib, nsmap, **_extra)
    result.text = text
    return result


class XMLPipeline(object):

    def process_item(self, item, spider):
        page = etree.Element('page', url=item['url'])
        for text in item['text_data']:
            if text:
                _create_sub_element(page, 'fragment', type='text', text=text)
        for src in item['images']:
            _create_sub_element(page, 'fragment', type='image', text=src)
        self.data.append(page)

    def open_spider(self, spider):
        self.data = etree.Element('data')
        self.doc = etree.ElementTree(self.data)

    def close_spider(self, spider):
        self.doc.write('output.xml', xml_declaration=True,
                       encoding='utf-16', pretty_print=True)

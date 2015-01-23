# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from scrapy.exceptions import DropItem

class ArtcollectionPipeline(object):
    def process_item(self, item, spider):
        return item


class DuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['reference'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            if item['artistbio'] and item['info']:
                self.ids_seen.add(item['reference'])
                return item
            else:
                raise DropItem("not Complete info")

class JsonWriterPipeline(object):

    def __init__(self):
        self.file = open('items.json', 'wb')

    def open_spider(self,spider):
        self.file.write('[')

    def close_spider(self,spider):
        self.file.write(']')
        file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + ",\n"
        self.file.write(line)
        return item

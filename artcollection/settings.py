# -*- coding: utf-8 -*-

# Scrapy settings for artcollection project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'artcollection'

SPIDER_MODULES = ['artcollection.spiders']
NEWSPIDER_MODULE = 'artcollection.spiders'
DUPEFILTER_CLASS = 'artcollection.myfilter.CustomFilter'
ITEM_PIPELINES = {
    'artcollection.pipelines.ArtcollectionPipeline': 300,
    'artcollection.pipelines.DuplicatesPipeline': 300,
    'artcollection.pipelines.JsonWriterPipeline':800,

}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'artcollection (+http://www.yourdomain.com)'

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import spiders
from spiders.twitterscrape import count
from dbtools.dbapi import *

class TwitterPipeline(object):
    def process_item(self, item, spider):
        global count
        keys = {k:v for k, v in item.iteritems()}

        #import ipdb; ipdb.set_trace()
        if spider.__class__ == spiders.twitterscrape.Scrapetwitterorganic:
            update_db_organic(item)

        if spider.__class__ == spiders.twitterscrape.Scrapetwitterfollowers:
            update_db_followers(item)

        if spider.__class__ == spiders.twitterscrape.Scrapetwitterhome:
            update_db_home(item)

        if spider.__class__ == spiders.twitterscrape.TweetsSpider:
            parse_csv(item)

        return item

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import db_settings

class LinkedinHistDataPipeline(object):

    def process_item(self, items, spider):
        return item


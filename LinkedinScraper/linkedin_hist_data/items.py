# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LinkedinHistDataItem(scrapy.Item):
	update_id = scrapy.Field()
	update_date = scrapy.Field()
	impressions = scrapy.Field()
	clicks = scrapy.Field()
	interactions = scrapy.Field()
	engagement = scrapy.Field()
	paid_impressions = scrapy.Field()
	paid_clicks = scrapy.Field()
	paid_interactions = scrapy.Field()
	paid_followers_acquired = scrapy.Field()
	paid_engagement = scrapy.Field()
	likes = scrapy.Field()
	comments = scrapy.Field()
	shares = scrapy.Field()
	url = scrapy.Field()
	update_text = scrapy.Field()
	title = scrapy.Field()
	comment = scrapy.Field()
	text = scrapy.Field()

class LinkedinFollowersItem(scrapy.Item):
	date = scrapy.Field()
	company_organic_followers = scrapy.Field()
	company_paid_followers = scrapy.Field()
	paid_diff = scrapy.Field()
	organic_diff = scrapy.Field()

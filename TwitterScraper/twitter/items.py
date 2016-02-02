# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TwitterItem(scrapy.Item):
    Tab = scrapy.Field()
    Fields = scrapy.Field()
    Categories = scrapy.Field()
    Percentage = scrapy.Field()
    Date = scrapy.Field()
    Total = scrapy.Field()
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class TwitterHomeItem(scrapy.Item):
    Month = scrapy.Field()
    Tweets = scrapy.Field()
    Tweet_impressions = scrapy.Field()
    Profile_visits = scrapy.Field()
    Mentions = scrapy.Field()
    New_followers = scrapy.Field()
    #Top_Tweet = scrapy.Field()
    #Top_Tweet_Impressions = scrapy.Field()
    #Top_Mention_by = scrapy.Field()
    #Top_Mention_Engagements = scrapy.Field()
    #Top_Follower = scrapy.Field()
    #Top_Follower_followed_by = scrapy.Field()
    Date = scrapy.Field()
    pass

class TweetsFile(scrapy.Item):
    tweets_file = scrapy.Field()
# Linkedin, Twitter historical data scraper and GA collector

Uses selenium+scrapy pipeline to receive data, and also `requests` library to work with HTTP and GA

 * `linkedin_hist_data/` - scrapy folder. Contains 3 linkedin spiders and 1 Twitter spider
   - `linkedin_spider` (`class LinkedinSpider`) - spider for company updates engagement data. Takes data from company updates feed
   - `linkedin_followers_spider` (`class LinkedinFollowers`) - scrapes data for followers tendencies. Data comes from analytics page
   - `linkedin_historical_data_spider` (`class LinkedinHistoricalData`) - takes historical engagements data per day from analytics page
   - `linkedin_demographics_data_spider` (`class LinkedinDemographicsData`) - *IS NOT USED*
   - `twitter_historical_date` (`class TwitterHistoricalData`) - parses twitter historical data from twitter analytics page

 * `legacy/` - this folder contains legacy data and scripts, that were used once for some reasons. 
 * `tools/` - currently contains one script, `feed_demographics.py`. Helps to interpolate linkedin demographics data if some part of it was occassionally lost
 * `demographics.py` - gets data about linkedin demographics from linkedin API
 * `ga_grabber.py` - used to get google analytics data for FB, Linkedin, Twitter

 ## Launch instructions

 - to launch crawlers
  	```
  		scrapy crawl <SPIDER_NAME>
   	```
 - to launch another tools
    ```
  		python <SCRIPT_NAME>
   	```
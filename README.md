# Social media extractor

Application that scrapes pages and wraps the API's of social media and saves this metrics into PostgreSQL on daily basis, launched via crontab

> Scrapers are using user credits, so don't forget to setup them. 

## Linkedin, Twitter historical data scraper and GA collector (LinkedinScraper)

Uses selenium+scrapy pipeline to receive data, and also `requests` library to work with HTTP and GA

 * `linkedin_hist_data/` - scrapy folder. Contains 3 linkedin spiders and 1 Twitter spider
   - `linkedin_spider` (`class LinkedinSpider`) - spider for company updates engagement data. Takes data from company updates feed
   - `linkedin_followers_spider` (`class LinkedinFollowers`) - scrapes data for followers tendencies. Data comes from analytics page
   - `linkedin_historical_data_spider` (`class LinkedinHistoricalData`) - takes historical engagements data per day from analytics page
   - `linkedin_demographics_data_spider` (`class LinkedinDemographicsData`) - *IS NOT USED*
   - `twitter_historical_date` (`class TwitterHistoricalData`) - parses twitter historical data from twitter analytics page
 * `linkedin_hist_data/db_settings.py` - config for database connectivity and definition of the models
 * `legacy/` - this folder contains legacy data and scripts, that were used once for some reasons. 
 * `tools/` - currently contains one script, `feed_demographics.py`. Helps to interpolate linkedin demographics data if some part of it was occassionally lost
 * `demographics.py` - gets data about linkedin demographics from linkedin API
 * `ga_grabber.py` - used to get google analytics data for FB, Linkedin, Twitter

> User data is placed in `ln_password` and `ln_account_email` of spider classes

### Launch instructions

 - to launch crawlers
   
        scrapy crawl <SPIDER_NAME>
   
 - to launch another tools

        python <SCRIPT_NAME>

### Crontab config

    cd <SCRAPER_PATH>
    PATH=$PATH:/usr/local/bin
    export PATH

    scrapy crawl linkedin_spider
    scrapy crawl linkedin_followers_spider
    scrapy crawl linkedin_historical_data_spider
    scrapy crawl twitter_historical_date
    python ga_grabber.py
    python demographics.py

    echo $(date) > /home/ec2-user/cron

## Twitter scraper (TwitterScraper)

 * `twitter` - folder with scrapers
 Contains only twitter specialized scrapers
   - `Scrapetwitterfollwers` (`class Scrapetwitterfollowers`) - scrapes twitter followers data
   - `Scrapetwitterorganic` (`class Scrapetwitterorganic`) - scrapes data for organic audience
   - `Scrapetwittertweets` (`class TweetsSpider`) - downloads csv file for tweets for last 28 days with detailed data about it
 * `twitter/dbtools` - contains API for working with db
   - `models.py` - definition of database models
   - `dbapi.py` - contains functions for working with db
   - `settings.py` - connection configuration

> To change user data to login in twitter, change it in such strings `driver.find_element_by_xpath('//*[@id="page-container"]/div/div[1]/form/fieldset/div[1]/input').send_keys("surferstat1")` for login and  `driver.find_element_by_xpath('//*[@id="page-container"]/div/div[1]/form/fieldset/div[2]/input').send_keys("soumen1001")` for password

### Launch instructions

 - to launch crawlers

         scrapy crawl <SPIDER_NAME>


### Crontab script

    cd <SCRAPER_PATH>
    PATH=$PATH:/usr/local/bin
    export PATH

    scrapy crawl Scrapetwitterfollwers
    scrapy crawl Scrapetwitterorganic
    scrapy crawl Scrapetwittertweets


## Facebook API wrapper (FacebookAPIWrapper)

 * `db` - contains models (`models.py`) and database connection config (`config.py`)
 * `constraints.py` - file with API credentials
 * `feed_wrapper.py` - parses Facebook posts feed
 * `wrapper.py <MODE>` - receives a rest of facebook data. Has two possible modes:
 	- `wrapper.py historical` - parses historical engagement and users data
 	- `wrapper.py country` - parses historical users data broken down by country

### Launch instructions


 * to launch scripts
    - `wrapper.py`:

    ```
	python wrapper.py <historical|country>
    ```

   - `feed_wrapper.py`:

   ```
	python feed_wrapper.py
   ```
   
### Crontab script


    /usr/bin/python <PATH_TO_SCRIPTS>/wrapper.py country
    /usr/bin/python <PATH_TO_SCRIPTS>/wrapper.py historical
    /usr/bin/python <PATH_TO_SCRIPTS>/feed_wrapper.py

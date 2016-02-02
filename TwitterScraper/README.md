# Twitter scraper

 * `twitter` - folder with scrapers
 Contains only twitter specialized scrapers
   - `Scrapetwitterfollwers` (`class Scrapetwitterfollowers`) - scrapes twitter followers data
   - `Scrapetwitterorganic` (`class Scrapetwitterorganic`) - scrapes data for organic audience
   - `Scrapetwittertweets` (`class TweetsSpider`) - downloads csv file for tweets for last 28 days with detailed data about it
 * `twitter/dbtools` - contains API for working with db
   - `models.py` - definition of database models
   - `dbapi.py` - contains functions for working with db
   - `settings.py` - connection configuration

## Launch instructions

 - to launch crawlers

```
	scrapy crawl <SPIDER_NAME>
```

## Crontab script

```
cd <SCRAPER_PATH>
PATH=$PATH:/usr/local/bin
export PATH

scrapy crawl Scrapetwitterfollwers
scrapy crawl Scrapetwitterorganic
scrapy crawl Scrapetwittertweets
```
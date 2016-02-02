# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import scrapy
from scrapy.contrib.spiders.init import InitSpider
from scrapy.http import Request, FormRequest
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import Rule
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.spider import BaseSpider
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.selector import HtmlXPathSelector
from selenium import webdriver
from ghost import Ghost
import time
import datetime
from twitter.items import TwitterItem
from twitter.items import TwitterHomeItem
from twitter.items import TweetsFile

from twitter.dbtools.models import *
from twitter.dbtools.settings import *
import requests

from datetime import date
import re
import os

from selenium.webdriver.common.action_chains import ActionChains

from pyvirtualdisplay import Display

count = 0

display = Display(visible=0, size=(800, 600))

# dirrectory where to save downloaded files
ROOT_DIR = '/home/ec2-user'

class Scrapetwitterfollowers(InitSpider):
    handle_httpstatus_list = [404]
    name = 'Scrapetwitterfollwers'
    allowed_domains = ['twitter.com','analytics.twitter.com']
    login_page = 'https://www.twitter.com/login'
    start_urls = ['https://analytics.twitter.com/accounts/8da3rj/audience_insights?audience_types=followers%2C&audience_interactions=%2C&audience_ids=*%2C&custom_types=%2C&targeting_criteria=[object+Object]%2C[object+Object]&attribute_group=overview']
    for_followers_amount = 'https://analytics.twitter.com/accounts/8da3rj/audience_insights?audience_types=followers,&audience_interactions=,&audience_ids=*,&custom_types=,&targeting_criteria=[object+Object],[object+Object]&attribute_group=overview'
    
    def get_cookies(self):
        driver = self.browser
        driver.implicitly_wait(15)
        base_url = "http://www.twitter.com"
        # redndering twitter page
        driver.get(base_url + "/login")

        # sending login credentials to form
        driver.find_element_by_xpath('//*[@id="page-container"]/div/div[1]/form/fieldset/div[1]/input').clear()
        driver.find_element_by_xpath('//*[@id="page-container"]/div/div[1]/form/fieldset/div[1]/input').send_keys("surferstat1")
        driver.find_element_by_xpath('//*[@id="page-container"]/div/div[1]/form/fieldset/div[2]/input').clear()
        driver.find_element_by_xpath('//*[@id="page-container"]/div/div[1]/form/fieldset/div[2]/input').send_keys("soumen1001")
        
        # clicking the button to submit
        driver.find_element_by_xpath('//*[@id="page-container"]/div/div[1]/form/div[2]/button').click()

        try :
            driver.implicitly_wait(15)
            # if you would be redirected to challenge page, this code handles it
            driver.find_element_by_xpath('//*[@id="challenge_response"]').clear()
            driver.find_element_by_xpath('//*[@id="challenge_response"]').send_keys('00447734904854')
            driver.find_element_by_xpath('//*[@id="email_challenge_submit"]').click()
            driver.implicitly_wait(15)
        except:
            pass
        cookies = driver.get_cookies()
        cookie_dic = {}
        for c in cookies:
            cookie_dic[c['name']] = c['value']
        #print cookies
        #print cookie_dic
        return cookie_dic

    
    def init_request(self):
        print '==========Start================'
        """This function is called before crawling starts."""
        return Request(url=self.login_page,
                       callback=self.login)

    def login(self, response):
        print '=======================LOGIN======================='
        """Generate a login request."""
        return [FormRequest.from_response(response,method='POST',formxpath='//*[@id="page-container"]/div/div[1]/form',
            formdata={'session[username_or_email]': 'surferstat1', 'session[password]': 'soumen1001'},
            callback=self.login_cookies)]
    
    def login_cookies(self, response):
        print '=======================COOKIES======================='
        
        return Request(url='https://analytics.twitter.com/accounts/8da3rj/audience_insights?audience_types=followers%2C&audience_ids=%2A%2C',
                       cookies=self.get_cookies(),callback=self.check_login_response)

    def check_login_response(self, response):
        print '=========Checking=============='
        """Check the response returned by a login request to see if we are
        successfully logged in.
        """
        if "@surferstat1" in response.body:
            self.log("Successfully logged in. Let's start crawling!")
            # Now the crawling can begin..
            #time.sleep(10)
            return self.initialized()
        else:
            self.log("Bad times :(")
            # Something went wrong, we couldn't log in, so nothing happens.

    def __init__(self):
        BaseSpider.__init__(self)
        # starting virtual display
        # comment this line if you are using desktop
        display.start()

        # estabilishing browser
        self.browser = webdriver.Firefox() 

    def parse(self, response):
        self.browser.get(response.url)

        time.sleep(5)
        self.browser.implicitly_wait(15)
        
        self.browser.implicitly_wait(15)

        hxs = Selector(text=self.browser.page_source)
        buttonpath= '//div[@id="audience-insights-panels"]/ul/li'

        buttons = hxs.xpath(buttonpath) # select rows
        followers = int(hxs.xpath('//*[@class="followers-size"]/b/text()').extract()[0].replace(',',''))
        
        count = followers

        # receiving historical followers data
        followers_by_date = self.parse_followers(hxs, count)
        items = []

        butt_num=1
        for button in buttons:
            # running through a tabs
            if butt_num==1:
                butt_num=butt_num+1
                continue
            
            button_click=buttonpath+'['+str(butt_num)+']/button'
            self.browser.find_element_by_xpath(button_click).click()
            page_name = button.xpath('button/div[1]/text()').extract()
            self.process(items,page_name,butt_num)
            
            butt_num=butt_num+1
        self.browser.close()
        for item in items:
            item['Total'] = count        
        display.stop() 
        return items

    def parse_followers(self, hxs, count):
        # this code parses data from the graph hover label using selenium
        arr = []
        length = len(hxs.xpath("//*[@class='barchart-chart']//*[@class='barchart-bar']").extract())
        for i in range(length-1):
            # selecting i-th bar in chart
            data = self.browser.find_element_by_xpath("//*[@class='barchart-chart']//*[@class='barchart-bar'][{0}]".format(i+1))
            
            # hovering on the bar chart
            ActionChains(self.browser).move_to_element(data).perform()
            self.browser.implicitly_wait(2)

            page_source = self.browser.page_source

            s = Selector(text=page_source)

            # receiving value from label
            arr.append(s.xpath("//*[@class='barchart-tooltip']//*[@class='barchart-tooltipvalue']/text()").extract()[0].replace(',',''))

        today = datetime.date.today()

        # Saving to db
        for i in range(len(arr)):
            date = today-datetime.timedelta(days=len(arr))+datetime.timedelta(days=i)
            value = int(arr[i])
            
            key = {}
            key['date'] = date
            item = session.query(TweetsOrganicFollowersTrends).filter_by(**key).first()

            if item:

                obj = item
            else:
                obj = TweetsOrganicFollowersTrends()
                obj.date = date

            obj.organic = value

            session.add(obj)
            session.commit()


    def parse_bar(self,vertical_table,items,page_name):
        # parses top bar
        category=vertical_table.xpath('div[1]/h4/text()').extract()
        rows=vertical_table.xpath('div[2]/div[2]/div')

        for row in rows:
            item = TwitterItem()
            item['Tab']=page_name
            item['Fields']=category
            item['Categories']=row.xpath("h6/text()").extract()
            item['Percentage']=row.xpath("h4/text()").extract()
            item['Date']=date.today()
            items.append(item)
        print item

    def process(self,items,page_name,button_index):
        # processes the rest of demographics data
        hxs = Selector(text=self.browser.page_source)
        
        tablepath= '//div[@id="audience-insights-panels"]/div['+str(button_index)+']/div[1]/div'
        left = hxs.xpath(tablepath) # select rows
     
        side_index=1
        for left_div in left:
            # looping through tabs
            if side_index==2:
                side_index=side_index+1
                continue
            tables=left_div.xpath('div')
            table_index=1
            for table in tables:
                category1=table.xpath('div[1]/h4/text()').extract()
                vertical_table=table.css('.vertical-bar-panel')
                if len (vertical_table)>0:
                    self.parse_bar(vertical_table,items,page_name)
                    continue
                rows = table.xpath('div[2]/table/tbody/tr')
                for row in rows:
                    item = TwitterItem()
                    item['Tab'] = page_name
                    item['Fields'] = category1
                    item['Categories']= row.select("td[1]/h4/text()").extract()
                    item['Percentage']= row.select("td[2]/h4/text()").extract()
                    item['Date']=date.today()

                    items.append(item)
                table_index=table_index+1
            side_index=side_index+1

# mostly similar to followers scraper, but only scans data about organic followers demographics
class Scrapetwitterorganic(InitSpider):
    handle_httpstatus_list = [404]
    name = 'Scrapetwitterorganic'
    allowed_domains = ['twitter.com','analytics.twitter.com']
    login_page = 'https://www.twitter.com/login'
    start_urls = ['https://analytics.twitter.com/accounts/8da3rj/audience_insights?audience_types=organic%2C&audience_interactions=impression%2C&audience_ids=506035855%2C&custom_types=%2C&targeting_criteria=%5Bobject+Object%5D%2C%5Bobject+Object%5D&attribute_group=overview']

    def get_cookies(self):

        driver = self.browser
        driver.implicitly_wait(15)
        base_url = "http://www.twitter.com"
        driver.get(base_url + "/login")
        driver.find_element_by_xpath('//*[@id="page-container"]/div/div[1]/form/fieldset/div[1]/input').clear()
        driver.find_element_by_xpath('//*[@id="page-container"]/div/div[1]/form/fieldset/div[1]/input').send_keys("surferstat1")
        driver.find_element_by_xpath('//*[@id="page-container"]/div/div[1]/form/fieldset/div[2]/input').clear()
        driver.find_element_by_xpath('//*[@id="page-container"]/div/div[1]/form/fieldset/div[2]/input').send_keys("soumen1001")
        driver.find_element_by_xpath('//*[@id="page-container"]/div/div[1]/form/div[2]/button').click()
        driver.implicitly_wait(15)
        try:
        	driver.find_element_by_xpath('//*[@id="challenge_response"]').clear()
       	 	driver.find_element_by_xpath('//*[@id="challenge_response"]').send_keys('447734904854')
        	driver.find_element_by_xpath('//*[@id="email_challenge_submit"]').click()
        	driver.implicitly_wait(15)
        except:
                pass
        cookies = driver.get_cookies()

        cookie_dic = {}
        for c in cookies:
            cookie_dic[c['name']] = c['value']
        return cookie_dic
        
    
    def init_request(self):
        print '==========Start================'
        """This function is called before crawling starts."""
        return Request(url=self.login_page,
                       callback=self.login)

    def login(self, response):
        print '=======================LOGIN======================='
        """Generate a login request."""
        return [FormRequest.from_response(response,method='POST',formxpath='//*[@id="page-container"]/div/div[1]/form',
            formdata={'session[username_or_email]': 'surferstat1', 'session[password]': 'soumen1001'},
            callback=self.login_cookies)]
    
    def login_cookies(self, response):
        print '=======================COOKIES======================='
        
        return Request(url='https://analytics.twitter.com/accounts/8da3rj/audience_insights?audience_types=organic%2C&audience_interactions=impression%2C&audience_ids=506035855%2C&custom_types=%2C&targeting_criteria=%5Bobject+Object%5D%2C%5Bobject+Object%5D&attribute_group=overview',
            cookies=self.get_cookies(),callback=self.check_login_response)

    def check_login_response(self, response):
        print '=========Checking=============='
        """Check the response returned by a login request to see if we are
        successfully logged in.
        """
        if "@surferstat1" in response.body:
            self.log("Successfully logged in. Let's start crawling!")
            # Now the crawling can begin..
            #time.sleep(10)
            return self.initialized()
        else:
            self.log("Bad times :(")
            # Something went wrong, we couldn't log in, so nothing happens.

    def __init__(self):
        BaseSpider.__init__(self)
        # use any browser you wish
        display.start()

        self.browser = webdriver.Firefox() 

    def parse(self, response):
        self.browser.get(response.url)
        
        # let JavaScript Load
        time.sleep(5)
        self.browser.implicitly_wait(15)        
        hxs = Selector(text=self.browser.page_source)
        buttonpath= '//div[@id="audience-insights-panels"]/ul/li'
        buttons = hxs.xpath(buttonpath) # select rows
        items = []
        butt_num=1
        for button in buttons:
            if butt_num==1:
                butt_num=butt_num+1
                continue
            button_click=buttonpath+'['+str(butt_num)+']/button'
            self.browser.find_element_by_xpath(button_click).click()
            page_name = button.xpath('button/div[1]/text()').extract()
            self.process(items,page_name,butt_num)
            
            butt_num=butt_num+1
        self.browser.close()
        display.stop()
        return items


    def parse_bar(self,vertical_table,items,page_name):
        category=vertical_table.xpath('div[1]/h4/text()').extract()
        rows=vertical_table.xpath('div[2]/div[2]/div')

        for row in rows:
            item = TwitterItem()
            item['Tab']=page_name
            item['Fields']=category
            item['Categories']=row.xpath("h6/text()").extract()
            item['Percentage']=row.xpath("h4/text()").extract()
            item['Date']=date.today()
            items.append(item)


    def process(self,items,page_name,button_index):
        hxs = Selector(text=self.browser.page_source)
        
        tablepath= '//div[@id="audience-insights-panels"]/div['+str(button_index)+']/div[1]/div'
        left = hxs.xpath(tablepath) # select rows
     
        side_index=1
        for left_div in left:
            if side_index==2:
                side_index=side_index+1
                continue
            tables=left_div.xpath('div')
            table_index=1
            for table in tables:
                category1=table.xpath('div[1]/h4/text()').extract()
                vertical_table=table.css('.vertical-bar-panel')
                if len (vertical_table)>0:
                    self.parse_bar(vertical_table,items,page_name)
                    continue
                rows = table.xpath('div[2]/table/tbody/tr')
                for row in rows:
                    item = TwitterItem()
                    item['Tab'] = page_name
                    item['Fields'] = category1
                    item['Categories']= row.select("td[1]/h4/text()").extract()
                    item['Percentage']= row.select("td[2]/h4/text()").extract()
                    item['Date']=date.today()

                    items.append(item)
                table_index=table_index+1
            side_index=side_index+1

# spider that takes data from downloaded file                  
class TweetsSpider(InitSpider):
    handle_httpstatus_list = [404]
    name = 'Scrapetwittertweets'
    allowed_domains = ['twitter.com','analytics.twitter.com']
    login_page = 'https://www.twitter.com/login'
    start_urls = ['https://analytics.twitter.com/user/DNVGL_Energy/tweets']

    def get_cookies(self):
        driver = self.browser
        driver.implicitly_wait(15)
        base_url = "http://www.twitter.com"
        driver.get(base_url + "/login")
        driver.find_element_by_xpath('//*[@id="page-container"]/div/div[1]/form/fieldset/div[1]/input').clear()
        driver.find_element_by_xpath('//*[@id="page-container"]/div/div[1]/form/fieldset/div[1]/input').send_keys("surferstat1")
        driver.find_element_by_xpath('//*[@id="page-container"]/div/div[1]/form/fieldset/div[2]/input').clear()
        driver.find_element_by_xpath('//*[@id="page-container"]/div/div[1]/form/fieldset/div[2]/input').send_keys("soumen1001")
        driver.find_element_by_xpath('//*[@id="page-container"]/div/div[1]/form/div[2]/button').click()
        driver.implicitly_wait(15)
        try:
            driver.find_element_by_xpath('//*[@id="challenge_response"]').clear()
            driver.find_element_by_xpath('//*[@id="challenge_response"]').send_keys('447734904854')
            driver.find_element_by_xpath('//*[@id="email_challenge_submit"]').click()
            driver.implicitly_wait(15)
        except:
        print 'Fail'

    cookies = driver.get_cookies()

        cookie_dic = {}
        for c in cookies:
            cookie_dic[c['name']] = c['value']
        return cookie_dic
    
    def init_request(self):
        print '==========Start================'
        """This function is called before crawling starts."""
        return Request(url=self.login_page,
                       callback=self.login)

    def login(self, response):
        print '=======================LOGIN======================='
        """Generate a login request."""
        return [FormRequest.from_response(response,method='POST',formxpath='//*[@id="page-container"]/div/div[1]/form',
            formdata={'session[username_or_email]': 'surferstat1', 'session[password]': 'soumen1001'},
            callback=self.login_cookies)]
    
    def login_cookies(self, response):
        print '=======================COOKIES======================='
        
        return Request(url='https://analytics.twitter.com/user/DNVGL_Energy/home',
            cookies=self.get_cookies(),callback=self.check_login_response)

    def check_login_response(self, response):
        print '=========Checking=============='
        """Check the response returned by a login request to see if we are
        successfully logged in.
        """
        if "@surferstat1" in response.body:
            self.log("Successfully logged in. Let's start crawling!")
            # Now the crawling can begin..
            #time.sleep(10)
            return self.initialized()
        else:
            self.log("Bad times :(")
            # Something went wrong, we couldn't log in, so nothing happens.

    def __init__(self):
        BaseSpider.__init__(self)
        # use any browser you wish
        display.start()

        profile = webdriver.FirefoxProfile()
        # setup configuration for browser driver to download file properly
        profile.set_preference("browser.download.folderList", 2)
        profile.set_preference("browser.download.manager.showWhenStarting", False)
        profile.set_preference("browser.download.dir", ROOT_DIR)
        profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/csv")

        self.browser = webdriver.Firefox(firefox_profile=profile) 

    def parse(self, response):
        # receiving url of analytics page
        self.browser.get(response.url)
        
        # let JavaScript Load
        time.sleep(5)
        self.browser.implicitly_wait(15)

        # clicking download button
        self.browser.find_element_by_xpath("//div[@id='export']/button").click()
        
        # waiting while file would be downloaded
        time.sleep(15)

        csv_file = filter(lambda x: re.match('.*.csv', x), os.listdir(ROOT_DIR))[0]

        item = TweetsFile()
        # remembering the path to downloaded file
        
        item['tweets_file'] =ROOT_DIR+'/'+csv_file
        
        self.browser.close()
        display.stop()
        return item

# Is not used
class Scrapetwitterhome(InitSpider):
    handle_httpstatus_list = [404]
    name = 'Scrapetwitterhome'
    allowed_domains = ['twitter.com','analytics.twitter.com']
    login_page = 'https://www.twitter.com/login'
    start_urls = ['https://analytics.twitter.com/user/DNVGL_Energy/home']

    def get_cookies(self):
        driver = self.browser
        driver.implicitly_wait(15)
        base_url = "http://www.twitter.com"
        driver.get(base_url + "/login")
        driver.find_element_by_xpath('//*[@id="page-container"]/div/div[1]/form/fieldset/div[1]/input').clear()
        driver.find_element_by_xpath('//*[@id="page-container"]/div/div[1]/form/fieldset/div[1]/input').send_keys("surferstat1")
        driver.find_element_by_xpath('//*[@id="page-container"]/div/div[1]/form/fieldset/div[2]/input').clear()
        driver.find_element_by_xpath('//*[@id="page-container"]/div/div[1]/form/fieldset/div[2]/input').send_keys("soumen1001")
        driver.find_element_by_xpath('//*[@id="page-container"]/div/div[1]/form/div[2]/button').click()
        driver.implicitly_wait(15)
        try:
        	driver.find_element_by_xpath('//*[@id="challenge_response"]').clear()
        	driver.find_element_by_xpath('//*[@id="challenge_response"]').send_keys('447734904854')
        	driver.find_element_by_xpath('//*[@id="email_challenge_submit"]').click()
        	driver.implicitly_wait(15)
	except:	
		pass
        cookies = driver.get_cookies()

        cookie_dic = {}
        for c in cookies:
            cookie_dic[c['name']] = c['value']
        return cookie_dic
        
    
    def init_request(self):
        print '==========Start================'
        """This function is called before crawling starts."""
        return Request(url=self.login_page,
                       callback=self.login)

    def login(self, response):
        print '=======================LOGIN======================='
        """Generate a login request."""
        return [FormRequest.from_response(response,method='POST',formxpath='//*[@id="page-container"]/div/div[1]/form',
            formdata={'session[username_or_email]': 'surferstat1', 'session[password]': 'soumen1001'},
            callback=self.login_cookies)]
    
    def login_cookies(self, response):
        print '=======================COOKIES======================='
        
        return Request(url='https://analytics.twitter.com/user/DNVGL_Energy/home',
            cookies=self.get_cookies(),callback=self.check_login_response)

    def check_login_response(self, response):
        print '=========Checking=============='
        """Check the response returned by a login request to see if we are
        successfully logged in.
        """
        if "@surferstat1" in response.body:
            self.log("Successfully logged in. Let's start crawling!")
            # Now the crawling can begin..
            #time.sleep(10)
            return self.initialized()
        else:
            self.log("Bad times :(")
            # Something went wrong, we couldn't log in, so nothing happens.

    def __init__(self):
        BaseSpider.__init__(self)
        # use any browser you wish
        display.start()

        self.browser = webdriver.Firefox() 

    def parse(self, response):
        self.browser.get(response.url)
        
        # let JavaScript Load
        time.sleep(5)
        self.browser.implicitly_wait(15)
        for i in range(1,15):
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(4)        
        hxs = Selector(text=self.browser.page_source)
        Path= '/html/body/div[4]/div/div[2]/div'
        panels = hxs.xpath(Path) # select rows
        items = []
        panel_num=1
        for panel in panels:
            if panel_num==1:
                panel_num=panel_num+1
                self.process(panel,items)
                continue
            print '=======till here======'
            item = TwitterHomeItem()
            month =  panel.xpath("div/h4[@class='home-dateline']/text()").extract()[0]
            m = month[re.finditer('\S+',month).next().start(0):]
            print(m)
            item['Month'] = m

            item['Tweets'] = panel.xpath("div[2]/div[2]/div/div/div/div[1]/div/div/text()").extract()
            item['Tweet_impressions'] = panel.xpath("div[2]/div[2]/div/div/div/div[2]/div/div/text()").extract()
            item['Profile_visits']= panel.xpath ("div[2]/div[2]/div/div/div/div[3]/div/div/text()").extract()
            item['Mentions'] = panel.xpath("div[2]/div[2]/div/div/div/div[4]/div/div/text()").extract()
            item['New_followers'] = panel.xpath("div[2]/div[2]/div/div/div/div[5]/div/div/text()").extract()
            #item['Top_Tweet'] = str(panel.xpath("div[2]/div[1]/div[1]/div[1]/div[1]/div/div[2]/div[1]/div/span/text()").extract()).strip()
            #item['Top_Tweet_Impressions'] = str(panel.xpath("div[2]/div[1]/div[1]/div[1]/div[1]/div/div[1]/h2/small/text()").extract()).strip()
            #item['Top_Mention_by'] = str(panel.xpath("div[2]/div[1]/div[1]/div[2]/div[1]/div/div[2]/div[1]/div/a/span[2]/text()").extract()).strip()
            #item['Top_Mention_Engagements'] = str(panel.xpath("div[2]/div[1]/div[1]/div[2]/div[1]/div/div[1]/h2/small/text()").extract()).strip()
            #item['Top_Follower'] = str(panel.xpath("div[2]/div[1]/div[1]/div[1]/div[2]/div/div[2]/div/div/div/div[2]/a/text()").extract()).strip()
            #item['Top_Follower_followed_by'] = str(panel.xpath("div[2]/div[1]/div[1]/div[1]/div[2]/div/div[1]/h2/small/text()").extract()).strip()
            item['Date']=date.today()
            items.append(item)
            print(item)
            print '=====Till Now======'
            panel_num=panel_num+1
        print panel_num  
        self.browser.close()
        display.stop()
        return items


    def process(self,panel_new,items):
        item = TwitterHomeItem()

        month =  panel_new.xpath("div/h4[@class='home-dateline']/text()").extract()[0]
        item['Month'] = month[re.finditer('\S+',month).next().start(0):]
        print(month)
        print(month[re.finditer('\S+',month).next().start(0):])

        item['Tweet_impressions'] = panel_new.xpath("div[2]/div[2]/div[2]/div/div/div[2]/div/div/text()").extract()
        item['Profile_visits']= panel_new.xpath ("div[2]/div[2]/div[2]/div/div/div[3]/div/div/text()").extract()
        item['Mentions'] = panel_new.xpath("div[2]/div[2]/div[2]/div/div/div[4]/div/div/text()").extract()
        item['New_followers'] = panel_new.xpath("div[2]/div[2]/div[2]/div/div/div[5]/div/div/text()").extract()
        #item['Top_Tweet'] = str(panel_new.xpath("div[2]/div[1]/div[1]/div[1]/div[1]/div/div[2]/div[1]/div/span/text()").extract()).strip()
        #item['Top_Tweet_Impressions'] = str(panel_new.xpath("div[2]/div[1]/div[1]/div[1]/div[1]/div/div[1]/h2/small/text()").extract()).strip()
        #item['Top_Mention_by'] = str(panel_new.xpath("div[2]/div[1]/div[1]/div[2]/div[1]/div/div[2]/div[1]/div/a/span[2]/text()").extract()).strip()
        #item['Top_Mention_Engagements'] = str(panel_new.xpath("div[2]/div[1]/div[1]/div[2]/div[1]/div/div[1]/h2/small/text()").extract()).strip()
        #item['Top_Follower'] = str(panel_new.xpath("div[2]/div[1]/div[1]/div[1]/div[2]/div/div[2]/div/div/div/div[2]/a/text()").extract()).strip()
        #item['Top_Follower_followed_by'] = str(panel_new.xpath("div[2]/div[1]/div[1]/div[1]/div[2]/div/div[1]/h2/small/text()").extract()).strip()
        item['Date']=date.today()
        items.append(item)

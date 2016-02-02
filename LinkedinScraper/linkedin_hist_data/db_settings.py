import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
'''
host = 'localhost'
user = 'nikita'
password = 'p@ssword'
db_name = 'social_data'
port = 8060
connection = engine = create_engine("postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}".format(
									user, password, host, port, db_name), echo=False)
'''

# config contstraints for postgresql connection
host = 'localhost'
user = 'roman'
password = '12345'
db_name = 'social_data'

# estabilishing connections
connection = engine = create_engine("postgresql+psycopg2://{0}:{1}@{2}/{3}".format(
									user, password, host, db_name), echo=False)

Base = declarative_base()
session = sessionmaker(bind=connection)()

# defining models

# Linkedin update data model 
class LinkedinHistoricalData(Base):
	__tablename__ = 'linkedin_historical_posts_data'
	update_id = Column(BigInteger, primary_key=True)
	update_date = Column(DateTime)
	scrape_date = Column(DateTime)
	impressions = Column(Integer)
	clicks = Column(Integer)
	interactions = Column(Integer)
	engagement = Column(Float)
	paid_impressions = Column(Integer)
	paid_clicks = Column(Integer)
	paid_interactions = Column(Integer)
	paid_followers_acquired = Column(Integer)
	paid_engagement = Column(Float)

	likes = Column(Integer)

	comments = Column(Integer)
	shares = Column(Integer)
	url = Column(String)
	update_text = Column(String)
	title = Column(String)
	comment = Column(String)
	total_update_text = Column(String)

class FollowersData(Base):
	__tablename__ = 'linkedin_followers_data'
	id = Column(Integer, primary_key=True)
	date = Column(Date)
	company_organic_followers = Column(Integer)
	company_paid_followers = Column(Integer)	
	paid_diff = Column(Integer)
	organic_diff = Column(Integer)

class FollowersByCountry(Base):
	__tablename__ = 'linkedin_followers_by_country_data'
	id = Column(Integer, primary_key=True)
	date = Column(Date)
	country = Column(String)
	value = Column(Integer)	
	
class HistoricalData(Base):
	__tablename__ = 'linkedin_historical_data'
	id = Column(Integer, primary_key=True)
	date = Column(Date)
	impressions = Column(Integer)
	clicks = Column(Integer)
	interactions = Column(Integer)
	engagement = Column(Float)
	paid_impressions = Column(Integer)
	paid_clicks = Column(Integer)
	paid_interactions = Column(Integer)
	paid_followers_acquired = Column(Integer)
	paid_engagement = Column(Float)
	paid_likes = Column(Float)
	paid_comments = Column(Float)
	paid_shares = Column(Float)
	likes = Column(Integer)
	comments = Column(Integer)
	shares = Column(Integer)

class CountriesData(Base):
	__tablename__ = 'linkedin_country_percentage_2'
	id = Column(Integer, primary_key=True)
	region_code = Column(String)
	created_at = Column(Date)
	share = Column(Float)

class LinkedinDemographics(Base):
	__tablename__ = 'linkedin_demographics_data'
	id = Column(Integer, primary_key=True)
	date = Column(Date)
	value = Column(Float)
	category = Column(String)
	name = Column(String)

# Twitter historical data definition
class TweetsHistoricalData(Base):
	__tablename__ = 'twitter_historical_data'
	id = Column(Integer, primary_key=True)
	date = Column(Date)
	impressions = Column(Integer)
	engagement_rate = Column(Float)
	retweets = Column(Integer)
	replies = Column(Integer)
	favorites = Column(Integer)
	tweets = Column(Integer)
	clicks = Column(Integer)

# GA data models definition
class LinkedinGAData(Base):
	__tablename__ = 'linkedin_ga_data'
	id = Column(Integer, primary_key=True)
	date = Column(Date)
	country = Column(String)
	percent = Column(Float)

class FacebookGAData(Base):
	__tablename__ = 'facebook_ga_data'
	id = Column(Integer, primary_key=True)
	date = Column(Date)
	country = Column(String)
	percent = Column(Float)

class TwitterGAData(Base):
	__tablename__ = 'twitter_ga_data'
	id = Column(Integer, primary_key=True)
	date = Column(Date)
	country = Column(String)
	percent = Column(Float)


Base.metadata.create_all(engine)

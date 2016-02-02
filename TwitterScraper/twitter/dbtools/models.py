from sqlalchemy import *
from settings import Base

# db models definition

class FollowerInfo(Base):
	__tablename__ = 'twitter_total_followers_demographics'

	id = Column(Integer, primary_key=True)
	category = Column(String)
	date = Column(Date)
	field = Column(String)
	value = Column(Integer)
	tab = Column(String)

class HomeInfo(Base):
	__tablename__ = 'db_home_info'

	id = Column(Integer, primary_key=True)
	date = Column(Date)
	mentions = Column(Integer)
	#TODO: ask about month
	month = Column(String)
	new_followers = Column(Integer)
	profile_visits = Column(Integer)
	tweet_impressions = Column(Integer)
	tweets = Column(Integer)

class OrganicInfo(Base):
	__tablename__ = 'twitter_organic_followers_demographics'

	id = Column(Integer, primary_key=True)
	category = Column(String)
	date = Column(Date)
	field = Column(String)
	percentage = Column(Integer)
	tab = Column(String)

class TweetsInfo(Base):
	__tablename__ = 'twitter_tweets_data'

	tweet_id = Column(String, primary_key=True)
	tweet_permalink = Column(String)
	tweet_text = Column(String)
	time = Column(Date)
	impressions = Column(Float)
	engagements = Column(Float)
	engagement_rate = Column(Float)
	retweets = Column(Float)
	replies = Column(Float)
	favorites = Column(Float)
	promoted_impressions = Column(Float)
	promoted_engagements = Column(Float)
	promoted_engagement_rate = Column(Float)
	promoted_retweets = Column(Float)
	promoted_replies = Column(Float)
	promoted_favorites = Column(Float)

class TweetsOrganicFollowersTrends(Base):
	__tablename__ = 'twitter_paid_organic_followers'
	id = Column(Integer, primary_key=True)
	date = Column(Date)
	organic = Column(Integer)
	paid = Column(Integer, default=0)

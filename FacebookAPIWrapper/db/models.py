
from db import *
from sqlalchemy import *

Base = config.Base

class FBStatistics(Base):
	__tablename__ = 'facebook_historical_data'
	id = Column(Integer, primary_key=True)
	date = Column(Date)
	impressions_organic = Column(Integer)
	impressions_paid = Column(Integer)
	clicks = Column(Integer)
	likes = Column(Integer)
	shares = Column(Integer)
	interactions = Column(Integer)
	visitors = Column(Integer)
	visitors_paid = Column(Integer)
	engagement = Column(Float)
	comments = Column(Integer)
	page_fans = Column(Integer)

		
class FBDemographics(Base):
	__tablename__ = 'facebook_demographic_data'
	id = Column(Integer, primary_key=True)
	date = Column(Date)
	
	category = Column(String)
	key = Column(String)
	value = Column(String)

class FBFansByCountry(Base):
	__tablename__ = 'facebook_fans_by_country'
	id = Column(Integer, primary_key=True)
	date = Column(Date)
	country = Column(String)
	value = Column(Integer)

class FBFansDemographics(Base):
	__tablename__ = 'facebook_fans_demographics'	
	id = Column(Integer, primary_key=True)
	date = Column(Date)
	
	category = Column(String)
	key = Column(String)
	value = Column(String)

class FBPost(Base):
	__tablename__ = 'facebook_posts'
	id = Column(String, primary_key=True)
	url = Column(String)
	date = Column(Date)
	likes = Column(Integer)
	message = Column(String)
	comments = Column(String)
	post_type = Column(String)
	impressions = Column(String)
Base.metadata.create_all(config.engine) 
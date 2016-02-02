from settings import *
from models import *
import datetime
import os
import csv
import datetime

Base.metadata.create_all(engine)

def update_db_organic(item):
	# updates the organic data
	key = {}
	key['date'] = datetime.date.today()
	
	key['tab'] = item['Tab'][0]
	key['field'] = item['Fields'][0]
	key['category'] = item['Categories'][0]

	instance = session.query(OrganicInfo).filter_by(**key).first()
	
	# handles "<1" metric in the analytics
	if '<' not in item['Percentage'][0]:
		key['percentage'] = int(item['Percentage'][0][:-1])
	else:
		key['percentage'] = 0

	key['date'] = item['Date']

	# checking if instance exists	
	if instance:

		instance.percentage = key['percentage']
		instance.date = key['date']
		session.add(instance)
	else: 
		new_instance = OrganicInfo()

		for k, v in key.iteritems():
			setattr(new_instance, k, v)

		session.add(new_instance)
	
	session.commit()

def update_db_followers(item):
	key = {}
	key['date'] = datetime.date.today()
	key['tab'] = item['Tab'][0]
	key['field'] = item['Fields'][0]
	key['category'] = item['Categories'][0]

	#import ipdb; ipdb.set_trace()
	instance = session.query(FollowerInfo).filter_by(**key).first()
	
	# handles "<1" metric in the analytics
	if '<' not in item['Percentage'][0]:
		print float(item['Percentage'][0][:-1])/100, item['Total']
		key['value'] = float(item['Percentage'][0][:-1])/100 * item['Total']
	else:
		key['value'] = 0.01* item['Total']

	key['date'] = item['Date']

	# check if instance exists
	if instance:
		instance.value = key['value']
		instance.date = key['date']

		session.add(instance)

	else: 

		new_instance = FollowerInfo()
		for k, v in key.iteritems():
			setattr(new_instance, k, v)

		session.add(new_instance)
	
	session.commit()

def promoted_parser(l):
	# while parsing tweets csv, handles "-" value field, which means "No data"
	if '-' in l:
		return 0
	else:
		return int(l)

def parse_csv(file):
	# parses and saves data from csv to database
	with open(file['tweets_file'], 'r+') as f:
		reader = csv.reader(f)
		reader.next()
		for row in reader:
			print(row)
			key = {}
			key['tweet_id'] = row[0]

			instance = session.query(TweetsInfo).filter_by(**key).first()
			# checks if instance exists. If so, updates it
			if instance:
				f = instance
			else:
				f = TweetsInfo()
				f.tweet_id = row[0]
			
			f.tweet_permalink = row[1]
			f.tweet_text = row[2]
			f.time = row[3]
			f.impressions = float(row[4])
			f.engagements = float(row[5])
			f.engagement_rate = float(row[6])
			f.retweets = float(row[7])
			f.replies = float(row[8])
			f.favorites = float(row[9])
			f.promoted_impressions = promoted_parser(row[22])
			f.promoted_engagements = promoted_parser(row[23])
			f.promoted_engagement_rate = promoted_parser(row[24])
			f.promoted_retweets = promoted_parser(row[25])
			f.promoted_replies = promoted_parser(row[26])
			f.promoted_favorites = promoted_parser(row[27])
			
			if not instance:
				session.add(f)
			session.commit()

		# removes csv file
		os.remove(file['tweets_file'])

# is not used 
def update_db_home(item):
	key = {}
	key['month'] = item['Month']
	#import ipdb; ipdb.set_trace()
	instance = session.query(HomeInfo).filter_by(**key).first()
	
	key['mentions'] = int(item['Mentions'][0].replace(',',''))
	key['new_followers'] = int(item['New_followers'][0].replace(',',''))
	key['profile_visits'] = int(item['Profile_visits'][0].replace(',',''))

	if 'K' in item['Tweet_impressions'][0]:
		key['tweet_impressions'] = float(item['Tweet_impressions'][0][:-1].replace(',','.'))*1000
	else:
		key['tweet_impressions'] = int(item['Tweet_impressions'][0].replace(',',''))

	key['date'] = item['Date']

	print(item)
	key['tweets'] = int(item['Tweets'][0] if 'Tweets' in item else 0)

	if instance:
		
		for k, v in key.iteritems():
			setattr(instance, k, v)

	else: 
		new_instance = HomeInfo()

		for k, v in key.iteritems():
			setattr(new_instance, k, v)

		session.add(new_instance)
	
	session.commit()

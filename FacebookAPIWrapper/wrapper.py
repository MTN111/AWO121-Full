import requests
import datetime
import re
import json
from db.config import *
from db.models import *

import sys

import constraints

API_URL = 'https://graph.facebook.com/v2.5/{0}/insights/{1}/{2}'

# contains parameters dicts for API request
keys_dict = {
	'impressions': {
		'period': 'day',
		'insight':'page_impressions',
		'id': constraints.PAGE_ID
	},
	'impressions_unique': {
		'period': 'day',
		'insight':'page_impressions_unique',
		'id': constraints.PAGE_ID
	},
	'impressions_paid': {
		'period': 'day',
		'insight':'page_impressions_paid',
		'id': constraints.PAGE_ID
	},
	'impressions_organic': {
		'period': 'day',
		'insight':'page_impressions_organic',
		'id': constraints.PAGE_ID
	},
	'stories': {
		'period': 'day',
		'insight':'page_stories',
		'id': constraints.PAGE_ID
	},
	'eng': {
		'period': 'day',
		'insight':'page_engaged_users',
		'id': constraints.PAGE_ID
	},
	'likes': {
		'period': 'day',
		'insight':'page_storytellers_by_story_type',
		'id': constraints.PAGE_ID
	},
	'demographics': {
		'id': constraints.PAGE_ID,
		'period':'day',
		'insight':'page_impressions_by_age_gender_unique'
	},
	'shares': {
		'id': constraints.PAGE_ID,
		'period':'day',
		'insight':'page_positive_feedback_by_type'
	},
	'clicks': {
		'id': constraints.PAGE_ID,
		'period':'day',
		'insight':'page_consumptions'	
	}, 
	'uniq_paid':{
		'period':'day',
		'id': constraints.PAGE_ID,
		'insight': 'page_impressions_paid_unique'
	},
	'uniq_org':{
		'period':'day',
		'id': constraints.PAGE_ID,
		'insight': 'page_impressions_organic_unique'
	},
	'fans':{
		'period':'lifetime',
		'id': constraints.PAGE_ID,
		'insight': 'page_fans'
	},
	'fans_demo': {
		'period':"lifetime",
		'id': constraints.PAGE_ID,
		'insight': 'page_fans_gender_age'
	},
	'fans_country': {
		'period':'lifetime',
		'id':constraints.PAGE_ID,
		'insight':'page_fans_country'
	}
}

def save_to_db( hist, demo, fans):
	# saving data as historical data
	for day in hist:
		key = {}
		key['date'] = day['date']
		ins = session.query(FBStatistics).filter_by(**key).first()
		
		# checking the existance
		if ins:
			obj = ins
		else: 
			obj = FBStatistics()

		# updating the model
		for k, v in day.iteritems():
			setattr(obj, k, v)

		session.add(obj)
		session.commit()
	
	def _(name, cls):
		# processing the data
		for k,v in day[name].iteritems():
			key['category'] = name
			key['key'] = k
			instance =  session.query(cls).filter_by(**key).first()

			# check for existance
			if instance:
				obj = instance
			else:
				obj = cls()
				obj.date = day['date']
				obj.category = name
				obj.key = k

			obj.value = v

			session.add(obj)
			session.commit()

	for day in demo:

		key = {}
		key['date'] = day['date']
		print day['date']
		
		# saving the demographics data
		_('gender',FBDemographics)
		_('age_groups',FBDemographics)


	for day in fans:

		key = {}
		key['date'] = day['date']

		# saving the demographics data for fans
		_('gender',FBFansDemographics)
		_('age_groups',FBFansDemographics)

def parse_demographics(data):
	# aggregating the data for day
	age_groups = {}
	gender_groups = {}

	for k,v in data['value'].iteritems():
		# finding the data about gender and age group
		pattern = re.match('^(?P<gender>[MUF])\.(?P<age_group>\S+)',k)
		
		gender = pattern.group('gender')
		age_group = pattern.group('age_group')
		
		if gender not in gender_groups:
			gender_groups[gender] = 0
		if age_group not in age_groups:
			age_groups[age_group] = 0
		
		age_groups[age_group] += v
		gender_groups[gender] += v

	return age_groups, gender_groups


def get_dict(metric_name, q_params):
	# receiving data list
	params = keys_dict[metric_name]

	response = requests.get(API_URL.format(params['id'], params['insight'], params['period']), params=q_params)
	_json = json.loads(response.text)

	# getting list of values
	if len(_json['data'])>0:
		return _json['data'][0]['values']
	else: 
		return []

def wrap():
	# wrapping the API
	today = datetime.date.today()
	until = (today-datetime.date(1970, 01,01)).total_seconds()
	date = (today-datetime.timedelta(days=89))
	since = (date-datetime.date(1970,1,1)).total_seconds()
	results = []

	while date > datetime.date(2015,07,01):
		# looping data for each day
		params = {
			'until': until,
			'since': since,
			'access_token': constraints.FB_API_KEY
		}

		until = (date - datetime.date(1970, 01, 01)).total_seconds()
		date = (date-datetime.timedelta(days=89))
		since = (date-datetime.date(1970,1,1)).total_seconds()

		# getting historical data
		data_imp = get_dict('impressions', params)
		data_org_imp = get_dict('impressions_organic', params)
		data_paid_imp = get_dict('impressions_paid', params)
		data_un = get_dict('impressions_unique', params)

		data_shares = get_dict('shares', params)
		data_stories = get_dict('stories', params)
		data_engaged_clicks = get_dict('eng', params)
		data_likes = get_dict('likes', params)
		data_demo = get_dict('demographics', params)
		data_clicks = get_dict('clicks', params)
		data_paid =  get_dict('uniq_paid', params)
		data_org = get_dict('uniq_org', params)

		results = []
		stats = []
		fans_arr= []

		# loop for each day
		for i in range(len(data_imp)):
			# parameters for fans for certain day 
			_date = datetime.datetime.strptime(data_imp[i]['end_time'][:10], '%Y-%m-%d')
			
			_params = params
			_params['since'] = (_date-datetime.timedelta(days=1)).strftime('%Y-%m-%d')
			_params['until'] = _date.strftime('%Y-%m-%d')

			# receiving fans for certain day
			fans = get_dict('fans', _params)

			print str(_date) + ' parsing'
			
			day = {'date':_date}
			day['impressions'] = data_imp[i]['value']
			day['impressions_organic'] = data_org_imp[i]['value']
			
			# handling data "holes"
			if 'value' in data_paid_imp[i]:
				day['impressions_paid'] = data_paid_imp[i]['value']
			else:
				day['impressions_paid'] = 0

			if day['impressions'] == 0:
				day['engagement'] = 0
			else:
				day['engagement'] = float(data_engaged_clicks[i]['value'])/data_un[i]['value'] or 0

			if 'fan' in data_likes[i]['value']:
				day['likes'] = data_likes[i]['value']['fan']
			else:
				day['likes'] = 0
			
			if 'link' in data_shares[i]['value']:
				day['shares'] = data_shares[i]['value']['link']
			else:
				day['shares'] = 0

			if 'comment' in data_shares[i]['value']:
				day['comments'] = data_shares[i]['value']['comment']
			else:
				day['comments'] = 0

			day['visitors'] = data_org[i]['value']
			day['visitors_paid'] = data_paid[i]['value']
			
			day['clicks'] = data_clicks[i]['value']
			val = 0

			for k, v in data_shares[i]['value'].iteritems():
				val+=v

			day['interactions'] = val	
			day['page_fans'] = fans[0]['value']
			day_demo = {'date':_date}
			results.append(day)

			demo = get_dict('fans_demo', _params)

			fans_demo = {'date':_date}
			
			if len(demo)>0:
				# processing demographics data for fans
				age_fans_groups, gender_fans_groups = parse_demographics(demo[0])
				
				fans_demo['age_groups'] = age_fans_groups
				fans_demo['gender'] = gender_fans_groups
				print (fans_demo)
				fans_arr.append(fans_demo)

			print day
			if len(data_demo) > 0:
				try:
					# processing demo data for impressions
					age_groups, gender_groups = parse_demographics(data[i])
					day_demo['gender'] = gender_groups
					day_demo['age_groups'] = age_groups
				except: 
					continue


			stats.append(day_demo)

			#import ipdb; ipdb.set_trace()
		print fans_arr
		# saving data to db
		save_to_db(results, stats, fans_arr)


def parse_fans_countries():
	# parses fans broken down by country
	today = datetime.date.today()
	date = today

	while date > (today - datetime.timedelta(years=2)+datetime.timedelta(days=1)):
		# looping for each day until today
		params = {
			'access_token': constraints.FB_API_KEY
		}
		params['since'] = (date-datetime.timedelta(days=1)).strftime('%Y-%m-%d')
		params['until'] = date.strftime('%Y-%m-%d')

		date = date-datetime.timedelta(days=1)

		# sending request
		data = get_dict('fans_country', params)	
		if len(data)>0:
			data = data[0]['value']
			for k, v in data.iteritems():
				# processing each row
				key = {
					'date':date,
					'country':k
				}

				# checking for existence
				inst = session.query(FBFansByCountry).filter_by(**key).first()
				if inst:
					obj = inst
				else:
					obj = FBFansByCountry()
					obj.date = key['date']
					obj.country = key['country']
				obj.value = v

				# creating / updating
				session.add(obj)
				session.commit()

if __name__ == '__main__':
	code = sys.argv[1]
	if code == 'country':
		parse_fans_countries()
	
	if code == 'historical':
		wrap()

from db.config import *
from db.models import *

import datetime
import constraints

import requests
import json

import re

LIKES_URL = 'https://graph.facebook.com/v2.5/{0}/likes'
COMMENTS_URL = 'https://graph.facebook.com/v2.5/{0}/comments'

API_URL = 'https://graph.facebook.com/v2.5/{0}/feed'
API_POST = 'https://graph.facebook.com/v2.5/{0}'
API_POST_IMPRESSION = 'https://graph.facebook.com/v2.5/{0}/insights/post_impressions'


LINK_URL = 'https://www.facebook.com/dnvglenergy/posts/'
UNIQUE_VISITORS = 'page_impressions_paid_unique'

INSIGHTS = 'post_impressions_fan'

def get_posts():
	# receiving the latest posts
	params = {'access_token': constraints.FB_API_KEY, 'limit': 100}
	response = requests.get(API_URL.format(constraints.PAGE_ID), params=params)
	json_dict = json.loads(response.text)
	
	params = {
		'access_token' : constraints.FB_API_KEY,
		'summary': True
	}

	# looping the each post in response
	for post in json_dict['data']:

		# post id
		id = re.match('(?P<page_id>\S+)_(?P<post_id>\S+)',post['id']).group('post_id')
		
		# receiving post from db
		instance = session.query(FBPost).get(id)
		
		# resolving engagement metrics for the post
		likes = json.loads(requests.get(LIKES_URL.format(post['id']), params=params).text)
		comments = json.loads(requests.get(COMMENTS_URL.format(post['id']),params=params).text)
		impressions = json.loads(requests.get(API_POST_IMPRESSION.format(post['id']),params=params).text)
		
		# check if post exists
		if instance :
			obj = instance
		else:
			obj = FBPost()
			obj.id = id

		obj.date = datetime.datetime.strptime(post['created_time'][:-5], '%Y-%m-%dT%H:%M:%S')
		
		# setting post type
		if 'message' in post:
			obj.message = post['message']
			obj.post_type = 'message'
		elif 'story' in post:
			obj.message = post['story']
			obj.post_type = 'story'
		else: 
			print str(post) + ' smth wrong'
			obj.message = ''

		obj.url = LINK_URL+id
		obj.likes = likes['summary']['total_count']
		obj.comments = comments['summary']['total_count']
		obj.impressions = impressions['data'][0]['values'][0]['value']

		session.add(obj)	
		session.commit()
	#import ipdb; ipdb.set_trace()

get_posts()

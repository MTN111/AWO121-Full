import requests
import json
import datetime
import time

import db_settings
from db_settings import *

client_secret = 'm4jffT1wrfbSCaX2O54Jpv_F'
client_id = '706670301433-0bt5s8pa4mcge5dpr9f13oapgrv5dut2.apps.googleusercontent.com'

credits = {u'refresh_token': u'1/ca6KTeHDgHSZ-lCIlgKLsgptGkuW_ESHThrP2r-4wYVIgOrJDtdun6zK6XiATCKT'}

REFRESHING_URL = 'https://www.googleapis.com/oauth2/v3/token'
ANALYTICS_API = 'https://www.googleapis.com/analytics/v3/data/ga' 

def get_auth_token():
	params = {
		'client_id': client_id,
		'access_type': 'offline',
		'response_type':'code',
		'redirect_uri':'http://localhost',
		'scope':'https://www.googleapis.com/auth/analytics.readonly',
	}
	t = requests.get(AUTH_URL, params=params)


#get_auth_token()
def token():
	refresh_token = credits['refresh_token']
	
	params = {
		'client_id' : client_id,
		'client_secret':client_secret,
		'redirect_uri':'http://localhost',
		'grant_type':'authorization_code',
		'code':'4/gjyYwbSPJJnMXew-qoK5r1iuu5Cf7bAlg96WF9y-81o'
	}

	response = requests.post(REFRESHING_URL, params=params)
	return response.json()['access_token'] 

#get_auth_token()
def refresh_token():
	refresh_token = credits['refresh_token']
	
	params = {
		'client_id' : client_id,
		'client_secret':client_secret,
		'refresh_token':refresh_token,
		'grant_type':'refresh_token'
	}

	response = requests.post(REFRESHING_URL, params=params)
	return response.json()['access_token'] 

def get_data(token):
	date = datetime.date.today()
	total = {'LinkedIn':[], 'Twitter':[], 'Facebook':[]}

	while True:
		end_date = date.strftime('%Y-%m-%d')
		date = (date - datetime.timedelta(days=30))
		start_date = date.strftime('%Y-%m-%d')

		if date < datetime.date(2015,03,05):
			break

		params = {
			'access_token' : token,
			'ids': 'ga:98670214',
			'start-date': start_date,
			'end-date': end_date,
			'dimensions':'ga:countryIsoCode,ga:socialNetwork,ga:date',
			'metrics':'ga:pageviews',
			'max-results':9999
		}

		response = requests.get(ANALYTICS_API, params=params)

		data = response.json()
		#print(data)
		rows = data['rows']
		print(len(rows))
		general = {'LinkedIn':[], 'Twitter':[], 'Facebook':[]}

		for x in rows:
			if x[1] in general:
				general[x[1]].append(x)
		buf = {}

		for k, v in general.iteritems():
			arr = {}
			for i in v: 
				row_date = datetime.datetime.strptime(i[2], '%Y%m%d')
				
				if row_date not in arr:
				 	arr[row_date] = []

				arr[row_date].append(i)

			buf[k] = arr
		general = buf

		for k, v in general.iteritems():
			buf[k] = {}
			arr_1 = []
			for k1, v1 in v.iteritems():
			
				sum = reduce(lambda x, y: x+int(y[3]),v1, 0)
				arr = map( lambda x: {'total':float(int(x[3]))/sum,'date': k1,'country':x[0]},v1)
				arr_1.append({'date':k1, 'countries':arr})
			buf[k] = arr_1
		
		for k, v in general.iteritems():
			for v1 in v:				
				total[k]+=v1['countries']

	session = db_settings.session

	for x in total['LinkedIn']:
		print x
		key = {}
		key['date'] = x['date']
		key['country'] = x['country']

		instance = session.query(LinkedinGAData).filter_by(**key).first()

		if instance :
			obj = instance
		else:
			obj = LinkedinGAData()
			obj.date = x['date']

		obj.country = x['country']
		obj.percent = x['total']
		
		session.add(obj)
		session.commit()


	for x in total['Twitter']:
		key = {}
		key['date'] = x['date']
		key['country'] = x['country']

		instance = session.query(TwitterGAData).filter_by(**key).first()

		if instance :
			obj = instance
		else:
			obj = TwitterGAData()
			obj.date = x['date']

		obj.country = x['country']
		obj.percent = x['total']
		
		session.add(obj)
		session.commit()
	
	for x in total['Facebook']:
		key = {}
		key['date'] = x['date']
		key['country'] = x['country']

		instance = session.query(FacebookGAData).filter_by(**key).first()

		if instance :
			obj = instance
		else:
			obj = FacebookGAData()
			obj.date = x['date']

		obj.country = x['country']
		obj.percent = x['total']
		
		session.add(obj)
		session.commit()

if __name__ == '__main__':

	token = refresh_token()
	get_data(token)

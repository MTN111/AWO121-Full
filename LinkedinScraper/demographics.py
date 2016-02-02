import requests
import json
import datetime
import codes

from linkedin_hist_data import db_settings

# Linkedin page credentials
LINKEDIN_KEY='77v2ofy2by41vh'
LINKEDIN_SECRET='763AeuKRTgaq6rjN'
LINKEDIN_PAGE_ID=5005117

API_URL = 'https://api.linkedin.com/v1/companies/{0}/company-statistics'
API_FOLLOWS_URL = 'https://api.linkedin.com/v1/companies/{0}/num-followers'

token = 'AQWMr0yoLD7TdOElkwyE78lgGXZhdQJiTy2VHVARVafxJmCmr1c-SCB38YwsTRYmrtohEes2sLfgzKUgbMBgLNa-ej8QtDIqYxne93MjiaUPoN4ogE2HvMS8l8MfrT2UdMihlzpSkM75bkxfjZzRgjB7PMSOjArL_i8i02HcGSUh-QN7YiA' 

headers = {
	'Authorization': 'Bearer '+token,
}

params = {
	'format':'json'
}

def get_data():
	response = requests.get(API_URL.format(LINKEDIN_PAGE_ID), params=params, headers=headers)
	data = json.loads(response.text)

	company_sizes = data['followStatistics']['companySizes']['values']
	functions = data['followStatistics']['functions']['values']
	seniorities = data['followStatistics']['seniorities']['values']
	industries = data['followStatistics']['industries']['values']
	countries = data['followStatistics']['countries']['values']

	def to_dict(data, category):
		# transforming data to dict, with changing some fields according to numerical constraints
		to_return = []
		for x in data:
			if category != 'COMPANY_SIZE':
				k = int(x['entryKey'])
			else:
				k = x['entryKey']
			to_return.append({
				'name': codes.CODES[category][k],
				'value': x['entryValue'],
				'category': category,
				'date': datetime.date.today()
			})
		return to_return
	
	def save_to_db(data):
		# saves data to db
		session = db_settings.session

		for x in data:
			key = {}

			key['date'] = x['date']
			key['name'] = x['name']
			key['category'] = x['category']

			ins = session.query(db_settings.LinkedinDemographics).filter_by(**key).first()

			if ins:
				obj = ins
			else:
				obj = db_settings.LinkedinDemographics()

			for k, v in x.iteritems():
				setattr(obj, k, v)

			session.add(obj)
			session.commit()

	def save_countries(data):
		session = db_settings.session
		date = datetime.date.today()
		# selecting only country codes for requests
		query_res = db_settings.engine.execute("select * from linkedin_geography_codes where code like '__.__';")
		query_res = query_res.fetchall()

		params = {
			'format': 'json',
		}

		for k in query_res[:3]:
			params['geos'] = k[0]
			# getting data from API for selected data
			response = requests.get(API_FOLLOWS_URL.format(LINKEDIN_PAGE_ID), params=params, headers=headers)
			value = int(response.text)

			key = {}
			key['date'] = date
			key['country'] = k[0][3:].upper()

			ins = session.query(db_settings.FollowersByCountry).filter_by(**key).first()

			print key['country']

			# checking if certain country data for current day is present
			if ins: 
				obj = ins
			else:
				# creating new db object
				obj = db_settings.FollowersByCountry()
				obj.date = key['date']
				obj.country = key['country']
			
			obj.value = value

			session.add(obj)
			session.commit()

	company_sizes = to_dict(company_sizes,'COMPANY_SIZE')
	functions = to_dict(functions,'FUNCTION')
	seniorities = to_dict(seniorities,'SENIORITY')
	industries = to_dict(industries,'INDUSTRY')

	# saving demographics data
	save_to_db(company_sizes)
	save_to_db(functions)
	save_to_db(seniorities)
	save_to_db(industries)
	# saving country data
	save_countries(countries)

get_data()

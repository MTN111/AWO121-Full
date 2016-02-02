import csv
import db_settings
import datetime

def parse_codes():
	with open('codes.csv','r+') as codes:
		reader = csv.reader(codes)
		reader.next()
		for row in reader:
			t = db_settings.CountriesData()

			t.created_at = datetime.datetime.strptime(row[0], "%m/%d/%Y").date()
			t.share = float(row[5])
			t.region_code = row[6].lower()

			db_settings.session.add(t)
			db_settings.session.commit()
parse_codes()

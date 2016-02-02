import numpy
from sqlalchemy import func
from linkedin_hist_data import db_settings

session = db_settings.session

# getting all possible demo categories
names = session.execute('select name,category from test_interpolation_view group by name, category')
names = names.fetchall()

for name in names:
	print name[0]
	data = session.execute("select date, value, category from test_interpolation_view where name='"+ name[0]+"';")
	# receiving all data about selected category
	data = data.fetchall()
	tointerpolate = []
	normal = []
	y = []
	for d in range(len(data)):
		if data[d][1] is None:
			# adding days without data
			tointerpolate.append(d)
		else:
			# adding days with data, to use for interpolation
			normal.append(d)
			y.append(data[d][1])

	# interpolating
	var = numpy.interp(tointerpolate, normal, y)

	for v in range(len(var)):
		# adding interpolated data to db
		obj = db_settings.LinkedinDemographics()

		obj.date = data[tointerpolate[v]][0]
		obj.value = int(var[v])
		obj.name = name[0]
		obj.category = name[1]
		id = session.query(func.max(db_settings.LinkedinDemographics.id)).first()[0]
		obj.id = id+1
		session.add(obj)
		session.commit()
		


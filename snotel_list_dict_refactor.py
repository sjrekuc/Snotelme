import csv
import requests
import os
# import mysql.connector

raw_file = 'raw.csv'
# get daily snow data from USDA
url='https://wcc.sc.egov.usda.gov/reportGenerator/view_csv/customMultipleStationReport/daily/network=%22SNTLT%22,%22SNTL%22%20AND%20element=%22SNWD%22%20AND%20outServiceDate=%222100-01-01%22%7Cname/0,0/name,stationId,WTEQ::value,WTEQ::delta,SNWD::value,SNWD::delta'
response = requests.get(url)

# read raw Request to clean CSV - eliminate comment rows with "#"
clean_file = 'clean.csv'
with open(clean_file, 'w') as fo:
	# r = response.text
	for line in response.iter_lines():
		t = str(line)
		if "#" not in t:
			fo.write(t)
			# write the row to a variable instead
			print(t)

### use CSV Dict Reader to read the Snotel locations into a list of dictionaries
with open('stat_loc.csv') as csv_loc:
	csv_reader = csv.DictReader(csv_loc, delimiter=',')
	line_count = 0
	locations = []
	for row in csv_reader:
		# if line_count > 0:
		locations.append(row)
		# d = {'Station Id': row['Station Id'], 'Station Name': row['Station Name'], 'Latitude': row['Latitude'], }
		line_count += 1


### use CSV Dict Reader to read in the snowfall into the list of dictionaries
with open(clean_file) as csv_snow:
	csv_reader = csv.DictReader(csv_snow, delimiter=',')
	line_count = 0
	for row in csv_reader:
		# if line_count > 0:
		for i in range(len(locations)):
			if locations[i]['Station Id'] == row['Station Id']:
				locations[i]['Snow Water Equivalent (in)'] = row['Snow Water Equivalent (in) Start of Day Values']
				locations[i]['Change In Snow Water Equivalent (in)'] = row['Change In Snow Water Equivalent (in)']
				locations[i]['Snow Depth (in)'] = row['Snow Depth (in) Start of Day Values']
				locations[i]['Change In Snow Depth (in)'] = row['Change In Snow Depth (in)']
		line_count += 1

## write that list of stations to a CSV that can be used on the website
with open('snow.csv', mode='w', newline='') as csv_combo:
	fieldnames = locations[0].keys()
	writer = csv.DictWriter(csv_combo, fieldnames=fieldnames)
	writer.writeheader()
	for j in range(len(locations)):
		writer.writerow(locations[j])


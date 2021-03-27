"""
This is written for python 2 in GoDaddy.

It gets data from snotel sites.

Then cleans the data by removing the commented section

We read in the location data of each station (pulled in the past)

"""


import csv
import requests
import os
from collections import OrderedDict 
# import mysql.connector

raw_file = 'raw.csv'
# get daily snow data from USDA
url='https://wcc.sc.egov.usda.gov/reportGenerator/view_csv/customMultipleStationReport/daily/network=%22SNTLT%22,%22SNTL%22%20AND%20element=%22SNWD%22%20AND%20outServiceDate=%222100-01-01%22%7Cname/0,0/stationId,WTEQ::value,WTEQ::delta,SNWD::value,SNWD::delta'
response = requests.get(url)
# read the CSV file first save before working with it more
with open(raw_file, 'wb') as f:
    for chunk in response:
        f.write(chunk)

# read the raw CSV back in and remove the commented lines
# open raw CSV
fi = open(raw_file, 'r')

# read raw CSV to clean CSV - eliminate comment rows with "#"
clean_file = 'clean.csv'
with open(clean_file, 'w') as fo:
    lines = fi.readlines()
    for line in lines:
        if "#" not in line:
            fo.write(line)
fi.close()


### use CSV Dict Reader to read the Snotel locations into a list of dictionaries
with open('stat_loc.csv') as csv_loc:
	csv_reader = csv.DictReader(csv_loc, delimiter=',')
	line_count = 0
	locations = []
	names = csv_reader.fieldnames
	for row in csv_reader:
		# if line_count > 0:
		d = OrderedDict(row)
		locations.append(d)
		# d = {'Station Id': row['Station Id'], 'Station Name': row['Station Name'], 'Latitude': row['Latitude'], }
		line_count += 1


### use CSV Dict Reader to read in the snowfall into the list of dictionaries
with open(clean_file) as csv_snow:
	csv_reader = csv.DictReader(csv_snow, delimiter=',')
	line_count = 0
	# iterates through the fieldnames to add them to the fieldname list for the final output
	for h in csv_reader.fieldnames:
	    # if the fieldname is not in the name, we add it
	    if h not in names:
	        names.append(h)
	print(names)
	for row in csv_reader:
		# if line_count > 0:
		for i in range(len(locations)):
			if locations[i]['Station Id'] == row['Station Id']:
				locations[i]['Snow Water Equivalent (in) Start of Day Values'] = row['Snow Water Equivalent (in) Start of Day Values']
				locations[i]['Change In Snow Water Equivalent (in)'] = row['Change In Snow Water Equivalent (in)']
				locations[i]['Snow Depth (in) Start of Day Values'] = row['Snow Depth (in) Start of Day Values']
				locations[i]['Change In Snow Depth (in)'] = row['Change In Snow Depth (in)']
		line_count += 1

## write that list of stations to a CSV that can be used on the website
with open('public_html/snow.csv', mode='w') as csv_combo:
	# uses fieldnames to maintain the order
	writer = csv.DictWriter(csv_combo, fieldnames=names)
	for j in range(len(locations)):
		writer.writerow(locations[j])


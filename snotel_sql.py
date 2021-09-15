import csv
import requests
import os
import mysql.connector
from collections import OrderedDict 

# # get daily snow data from USDA
url='https://wcc.sc.egov.usda.gov/reportGenerator/view_csv/customMultipleStationReport/daily/network=%22SNTLT%22,%22SNTL%22%20AND%20element=%22SNWD%22%20AND%20outServiceDate=%222100-01-01%22%7Cname/0,0/name,stationId,WTEQ::value,WTEQ::delta,SNWD::value,SNWD::delta'
raw_file = 'raw.csv'
response = requests.get(url)

# connect to the database
mydb = mysql.connector.connect(
  host="localhost",

)

mycursor = mydb.cursor()
# mycursor.execute("UPDATE Snow SET water = $s WHERE Station_Id = %s ", (l[2], int(l[1])))

# function to clean the inputs for the database
def clean_up(num):
    try:
        return float(num)
    except:
        return 0

# loops through the response and updates those values in the SQL DB
i=0
for line in response.text.splitlines():
    if '#' not in line:
        l = line.split(',')
        if i > 0:
            v = (clean_up(l[2]), clean_up(l[3]), clean_up(l[4]), clean_up(l[5]), int(l[1]))
            # mycursor.execute("SELECT * FROM Snow WHERE Station_Id = %s ", (int(l[1]),)) # this works - prints all stations
            # mycursor.execute("UPDATE Snow SET water = %s WHERE Station_Id = %s ", (v[0], v[4])) # this works - updates the water at each station
            mycursor.execute("UPDATE Snow SET water = %s, precip = %s, depth = %s, snow = %s WHERE Station_Id = %s ", v)
            mydb.commit()
        print(i)
        i+=1


mycursor.execute("SELECT * FROM Snow WHERE snow IS NOT NULL")
for x in mycursor:
	print(x)

mycursor.execute("SELECT COUNT(snow) FROM Snow")
for x in mycursor:
	print(x)
	
# write the snotel data from the DB to a CSV so we can use with the current JS code

## write that list of stations to a CSV that can be used on the website
with open('public_html/snow2.csv', mode='w') as csv_combo:
	# uses fieldnames to maintain the order
	writer = csv.writer(csv_combo)
	mycursor.execute("SELECT * FROM Snow WHERE snow IS NOT NULL")
	for j in mycursor:
		writer.writerow(j)




### use CSV Dict Reader to read in the snowfall into the list of dictionaries
# with open(clean_file) as csv_snow:
# 	csv_reader = csv.DictReader(csv_snow, delimiter=',')
# 	line_count = 0
# 	# iterates through the fieldnames to add them to the fieldname list for the final output
# 	for h in csv_reader.fieldnames:
# 	    # if the fieldname is not in the name, we add it
# 	    if h not in names:
# 	        names.append(h)
# 	print(names)
# 	for row in csv_reader:
# 		# if line_count > 0:
# 		for i in range(len(locations)):
# 			if locations[i]['Station Id'] == row['Station Id']:
# 				locations[i]['Snow Water Equivalent (in) Start of Day Values'] = row['Snow Water Equivalent (in) Start of Day Values']
# 				locations[i]['Change In Snow Water Equivalent (in)'] = row['Change In Snow Water Equivalent (in)']
# 				locations[i]['Snow Depth (in) Start of Day Values'] = row['Snow Depth (in) Start of Day Values']
# 				locations[i]['Change In Snow Depth (in)'] = row['Change In Snow Depth (in)']
# 		line_count += 1
	
# ### use CSV Dict Reader to read the Snotel locations into a list of dictionaries
# with open('stat_loc.csv') as csv_loc:
# 	csv_reader = csv.DictReader(csv_loc, delimiter=',')
# 	line_count = 0
# 	locations = []
# 	names = csv_reader.fieldnames
# 	for row in csv_reader:
# 		# if line_count > 0:
# 		d = OrderedDict(row)
# 		locations.append(d)
# 		# d = {'Station Id': row['Station Id'], 'Station Name': row['Station Name'], 'Latitude': row['Latitude'], }
# 		line_count += 1

# print(len(locations))

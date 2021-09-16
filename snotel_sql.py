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
        i+=1


# mycursor.execute("SELECT * FROM Snow WHERE snow IS NOT NULL")
# for x in mycursor:
# 	print(x)

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

	


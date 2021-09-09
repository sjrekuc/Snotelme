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
  database="Snotel"
)

mycursor = mydb.cursor()
mycursor.execute("UPDATE Snow SET water = $s WHERE Station_Id = %s ", (l[2], int(l[1])))


i=0
for line in response.text.splitlines():
    if '#' not in line:
        l = line.split(',')
        if i > 0:
            v = (l[2], l[3], l[4] or 0, l[5] or 0, int(l[1]))
            print(v)
            # mycursor.execute("SELECT * FROM Snow WHERE Station_Id = %s ", (int(l[1]),)) # this works
            mycursor.execute("UPDATE Snow SET water = $s WHERE Station_Id = %s ", (l[2], int(l[1])))
            db.commit()
            # mycursor.execute("UPDATE Snow SET water = $s, precip = %s, depth = %s, snow = %s WHERE Station_Id = %s ", (l[2], l[3], l[4] or 0, l[5] or 0, int(l[1])))
            # mycursor.execute("UPDATE Snow SET (water, precip, depth, snow) VALUES (%s, %s, %s, %s) WHERE Station_Id = %s ;", v)
            # for x in mycursor:
	           # print(x)
	       
        i+=1
# print(response.text)

# lines = response.text.split()
# for line in lines:
#     print(line)



# # read the CSV file first save before working with it more
# with open('raw.csv', 'wb') as f:
#     for chunk in response.text:
#         f.write(chunk)
#         print(chunk)

# read the raw CSV back in and remove the commented lines
# open raw CSV
# fi = open(raw_file, 'r')

# # read raw CSV to clean CSV - eliminate comment rows with "#"
# clean_file = 'clean.csv'
# with open(clean_file, 'w') as fo:
#     lines = fi.readlines()
#     for line in lines:
#         if "#" not in line:
#             fo.write(line)
# fi.close()


# ### need to figure out SQL from here on out.

# connect to the database
# mydb = mysql.connector.connect(
#   host="localhost",
#   user="srekuc",
#   password="Yay!Utah21",
#   database="Snotel"
# )

# mycursor = mydb.cursor()

# query
# mycursor.execute("UPDATE Snow () VALUES (%s, %s, %s, %s) WHERE Station_Id = ", t)
# mycursor.execute("UPDATE Snow () VALUES (%s, %s, %s, %s) WHERE Station_Id = ", t)


for x in mycursor:
	print(x)
	

### loads the snowfall clean file and adds it to the DB
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
	
	
	

# # load the station information from CSV so that it can be added to the MySQL DB
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

# ##### Updating the tables with the new snow data
# mycursor = mydb.cursor()



# Inserting the location data into the tables
# mycursor = mydb.cursor()
# count = 0;
# for d in locations:
#     t = (d['Station Id'], d['Station Name'], d['Latitude'], d['Longitude'])
#     print(t)
#     # count +=1
#     # if count > 5:
#     #     break
#     mycursor.execute("INSERT INTO Snow (Station_Id, Station_Name, latitude, longitude) VALUES (%s, %s, %s, %s)", t)


#### Delete query
# mycursor = mydb.cursor()
# mycursor.execute("DELETE FROM Snow WHERE Station_Id = '301' & Snow = 'Null'; ") #  


# mycursor.executemany("INSERT INTO Snow (Station_Id, Station_Name, latitude, longitude, water, precip, depth, snow) VALUES (%s, %s)", locations)


# # read that CSV to a DF
# snow = pd.read_csv(clean_file, error_bad_lines=False)

# # read the location data from that CSV
# loc_file = 'stat_loc.csv'
# loc = pd.read_csv(loc_file, error_bad_lines=False)

# # merge the location and snowfall data
# df = pd.merge(loc, snow, on="Station Id", how='left')
# df.drop('Station Name_y', axis=1, inplace=True)

# # export that data to the CSV to use for website
# df.to_csv("snow.csv", index=False)
import csv
import requests
import os
import mysql.connector

# # get daily snow data from USDA
# url='https://wcc.sc.egov.usda.gov/reportGenerator/view_csv/customMultipleStationReport/daily/network=%22SNTLT%22,%22SNTL%22%20AND%20element=%22SNWD%22%20AND%20outServiceDate=%222100-01-01%22%7Cname/0,0/name,stationId,WTEQ::value,WTEQ::delta,SNWD::value,SNWD::delta'
# raw_file = 'raw.csv'
# response = requests.get(url)
# # read the CSV file first save before working with it more
# with open('raw.csv', 'wb') as f:
#     for chunk in response:
#         f.write(chunk)

# # read the raw CSV back in and remove the commented lines
# # open raw CSV
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



mydb = mysql.connector.connect(
  host="localhost",
  user="sjrekuc",
  password="Yay!Utah21",
  database="Snotel"
)

print(mydb)

mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE sites (Station Id INT, Station Name VARCHAR(255), Latitude FLOAT(8), Longitude FLOAT(8), SWE FLOAT(6), SWE_ch FLOAT(5), Depth FLOAT(7), Snow FLOAT(6))")

mycursor.execute("SHOW TABLES")

for x in mycursor:
	print(x)


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
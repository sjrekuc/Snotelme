# Snotelme
Google mapping of snotel snow reports.

This will be available on the web at snotelme.com and snowtellme.com. Currently hosted on GoDaddy Servers with cPanel.

Files: <br>

Snotel.ipynb - Jupyter Notebook used to explore this concept of seeing the snowfall data from Snotel sites. Used this notebook to pull the location of all snotel sites and stored that site data in a CSV (stat_loc.csv). Since this is static information, we use this CSV again in snotel_list_dict.py to create the CSV that combines the station location along with the new snow report.

stat_loc.csv - CSV containing the location (lat and long) of all the snotel sites throughout the western US. This data is static and will be used by the next python file to combine with the daily snowfall and be mapped finally.

snotel_list_dict.py - python file that pulls takes pulls all of the daily snowfall updates from snotel sites throughout the western US. It then combines these snowfall reports with the location of the snotel sites that are contained in the CSV.

snow_2021-02-09.csv - sample CSV file from February 9th that show the snow report for that day with station location data. This CSV is ready to plot in using the HTML and JS files that come next.

snotelme.html - contain the HTML to just map the snotel sites and their snowfall total on a Google Map. JavaScript is necessary to make this work - see the next file on the list.

snowtellme.js - this is the JS code that works with html to plot the snow reports throughout the western US.



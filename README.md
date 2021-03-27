# Snotelme
Google mapping of snotel snow reports.

This will be available on the web at snotelme.com and snowtellme.com. Currently hosted on GoDaddy Servers with cPanel.

Files:
snotel_list_dict.py - python file that pulls takes pulls all of the daily snowfall updates from snotel sites throughout the western US. It then combines these snowfall reports with the location of the snotel sites that are contained in the CSV.

snotelme.html - contain the HTML to just map the snotel sites and their snowfall total on a Google Map. JavaScript is necessary to make this work - see the next file on the list.

snowtellme.js - this is the JS code that works with html to plot the snow reports throughout the western US.



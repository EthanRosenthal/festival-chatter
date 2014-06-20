# -*- coding: utf-8 -*-
"""
Created on Sun June 15 15:38:10 2014

@author: Ethan

This routine goes to the Bonnaroo website and scrapes the band schedule.
The band, date, and performance time are collected and inserted into a 
mongodb database.
"""

import urllib2
from BeautifulSoup import BeautifulSoup
import pymongo

# Connect to local mongodb database
db = pymongo.MongoClient().bonarooSchedule

# URL for first day's schedule
scheduleUrls=['http://lineup.bonnaroo.com/events/2014/06/12/']

day = 13

# Build list of URL's for each day's schedule
while day<16: 
	scheduleUrls.append('http://lineup.bonnaroo.com/events/2014/06/'+str(day)+'/')
	day+=1

for url in scheduleUrls: # for each day
	ufile = urllib2.urlopen(url)
	soup = BeautifulSoup(ufile)
	eventTable = soup.findAll('div',{'class':'ds-event-container'})

	for events in eventTable:
		# Build data dict to insert into database
		data={}
		try:
			data['band'] = events.find('a').text
			data['band_Error'] = 0
		except (ValueError,AttributeError):
			# Some bands were were not listed
			data['band'] = 'Error: See HTML \n' + str(events)
			data['band_Error'] = 1

		data['date'] = ''.join(url.split('/')[-4:-1]) # Grab date from end of URL		
		
		try:
			data['time'] = events.find('span',{'class':'ds-time-range'}).text
			data['time_Error'] = 0
		except (ValueError,AttributeError):
			# Some band times were "TBA"
			data['time'] = 'Error: See HTML \n' + str(events)
			data['time_Error'] = 1

		db.Bands.insert(data)
    
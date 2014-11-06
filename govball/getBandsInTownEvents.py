# -*- coding: utf-8 -*-
"""
Created on Mon May 26 22:41:12 2014

This routine takes the list of bands and their MusicBrainzID's and grabs all
concerts that they're performing between 01/01/2014 and 09/30/2014.

All of the information about the concerts is inserted into a mongodb database.

@author: Ethan
"""

import urllib2
import json
import pymongo


parent_url = 'http://api.bandsintown.com/artists/'
db = pymongo.MongoClient().BandsInTown


with open('MusicBrainzIDList.txt','r') as fin:
    for bands in fin:
        artist,mbid = bands.rstrip('\n').split(':')
        artist = artist.replace(' ','%20') #For inserting into URL below
        try:
            # Sends API request using MusicBrainzID of the artist
            request = urllib2.urlopen(parent_url+artist+'/events.json?artist_id=mbid_'+ 
            mbid+'api_version=2.0&app_id=GovBallTrack&date=2014-01-01,2014-09-30')
        except:
            print 'Could not find artist ' + artist +'\n'
            continue
        request=json.load(request)
        data={}
       
       # If there's no events, then request=[] The below will make sure the
       # artist name is still logged.
        try:
            data['artist'] = request[0]['artists'][0]['name']
        except:
            data['artist'] = artist.replace('%20',' ')
            
        eventList=[]
        
        #Build event dictionary 
        for events in request:
            date=events['datetime'].split('T')[0] #Gets rid of time. Just YYY-MM-DD
            venue=events['venue']['name']
            city=events['venue']['city']
            region=events['venue']['region'] #State for USA
            country=events['venue']['country']
            latitude=events['venue']['latitude']
            longitude=events['venue']['longitude']
            eventList.append({'date':date,'venue':venue,'city':city,
            'region':region,'country':country,'latitude':latitude,
            'longitude':longitude})
            
        data['events'] = eventList
        db.Artists.insert(data)
        
    fin.close()
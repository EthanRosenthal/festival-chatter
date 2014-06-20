# -*- coding: utf-8 -*-
"""
Created on Sun May 25 14:31:41 2014
This routine 

@author: Ethan
"""

import musicbrainzngs as mbrainz

mbrainz.auth('','') # Omitted for github
mbrainz.set_useragent('','') # Omitted for github



with open('BandList.txt','r') as fin:
    with open('MusicBrainzIDList.txt','w') as fout:
        for bands in fin:
            bands=bands.rstrip('\n')
            result=mbrainz.search_artists(artist=bands,limit=1)
            for artist in result['artist-list']:                
                fout.write(artist['name'].encode('ascii','ignore')+':'+artist['id'].encode('ascii','ignore')+'\n')
        
    fout.close()
fin.close()
                
            
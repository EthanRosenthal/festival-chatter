# -*- coding: utf-8 -*-
"""
Created on Sun May 25 14:53:10 2014

@author: Ethan

This routine goes to the Bonnaroo website, creates a list 
containing every band performing and writes this list out
to a file.
"""

import urllib2
from BeautifulSoup import BeautifulSoup



url='http://lineup.bonnaroo.com/'

ufile = urllib2.urlopen(url)

soup = BeautifulSoup(ufile)

bandList = soup.find('div',{'class':'ds-lineup ds-player'}).findAll('a')

fout = open('bonnarooBandList.txt','w')

for row in bandList:
	band=row.renderContents()
	fout.write(band + '\n')
    
    
fout.close()
    
# -*- coding: utf-8 -*-
"""
Created on Sun May 25 14:53:10 2014

@author: Ethan
"""

import urllib2
from BeautifulSoup import BeautifulSoup



url='http://lineup.governorsballmusicfestival.com/'

ufile = urllib2.urlopen(url)

soup = BeautifulSoup(ufile)

bandList = soup.findAll('li',{'class':'w'})

fout = open('BandList.txt','w')

for rows in bandList:
    band=rows.find('a')

    fout.write(band.text.encode('ascii','ignore')+'\n')
    
    
fout.close()
    
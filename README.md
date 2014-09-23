festival-chatter
================

This is a personal project to learn data science by analyzing summer music festivals. So far, there are two music festival directories: Governor's Ball and Bonnaroo.

The aim of the project is twofold - I would like to learn R and natural language processing to analyze twitter data, and I would like to learn new visualization libraries like d3.js.

* For analyzing twitter data, there is a python routine to connect to the Streaming Twitter API. I stored tweets related to Bonnnaroo, during Bonnaroo, in a mongodb database. There is another python routine to scrape the Bonnaroo website to get the band list and the performance schedule. I am currently analyzing the collected database to learn about band popularity and attendee sentiments during the festival.

* For visualization, I would like to create touring maps of the bands performing Governor's Ball to see how they all converged on NYC. There is python code to scape the Governor's Ball website to get a list of performers. I use the performer names to query the MusicBrainz database to get unique identifiers to then query the BandsInTown API to get individual band's touring information over a selected date range.


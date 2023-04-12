#si206 final project
import math 
import re
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import os
import sqlite3
import unittest
import requests

#beautiful soup portion 
def parse_web_with_soup(website):

    url = 'https://chartmasters.org/most-streamed-artists-ever-on-spotify/'
    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find('div', class_='wpdt-c wdt-skin-light')

    rows = table.find_all('tr')[1:]

# Create an empty list to hold the artist-streams tuples
    artist_streams = []

# Loop through each row and extract the artist and their total streams
    for row in rows:
      cols = row.find_all('td')
      artist = cols[2].text.strip()
      artist = artist.re
      streams = cols[3].text.strip()
      artist_streams.append((artist, streams))


    top10_artists = artist_streams[:10]


    print(top10_artists)



#read in the soup 




#read the website (chartmasters)



#get top 10 artists 




#get their total spotify streams 


def main():
    parse_web_with_soup("https://chartmasters.org/most-streamed-artists-ever-on-spotify/")



if __name__ == '__main__':
    main()


#si206 final project
import math 
import re
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import os
import sqlite3
import unittest
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

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
    counter = 0
    for row in rows :
      if counter == 10:
        break
      cols = row.find_all('td')
      artist = cols[2].contents
      artist = artist[0].contents
      artist = artist[0].contents
   
      streams = cols[3].text.strip()
      artist_streams.append((artist, streams))
      counter += 1



    top10_artists = artist_streams[:10]


    return top10_artists



#read in the soup 




#read the website (chartmasters)



#get top 10 artists 

#get top 10 songs
def top_ten_songs(top10_artists):
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id='insert client_id',
                                                           client_secret='insert client_secret'))
    
    names_only = []
    for item in top10_artists:
        name = item[0][0]
        names_only.append((name))


    #need help getting artist id
    list_artist = ('3TVXtAsR1Inumwj472S9r4','4q3ewBCX7sLwd24euuV69X','06HL4z0CvFAxyc27GXpf02','6eUKZXaKkcviH0Ku9w2n3V','1Xyo4u8uXC1ZmMpatF05PJ','1uNFoZAHBGtllmzznpCI3s','66CXWjxzNUsdJxJ2JdwvnR','7dGJo4pcD2V6oG8kP0tJRR','3Nrfpe0tUJi4K4DXYWgMUX','246dkjvS1zLTtiykXe5h60')

    total_top10_songs = []
    indiv_top10_songs = []

    for artist in list_artist:
        result = sp.artist_top_tracks(artist)
        for track in result['tracks'][:10]:
            songs = track['name']
            total_top10_songs.append(songs)

    for i in range(0, len(total_top10_songs), 10):
        group = total_top10_songs[i:i + 10]
        indiv_top10_songs.append(tuple(group))
    
    top10_by_artist = []
    for i in range(len(names_only)):
        top10_by_artist.append((names_only[i], indiv_top10_songs[i]))

    print(top10_by_artist)


#get their total spotify streams 


def main():
    top_artists = parse_web_with_soup("https://chartmasters.org/most-streamed-artists-ever-on-spotify/")
    top_ten_songs(top_artists)



if __name__ == '__main__':
    main()


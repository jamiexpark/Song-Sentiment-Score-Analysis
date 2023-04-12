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


    print(top10_artists)



#read in the soup 




#read the website (chartmasters)



#get top 10 artists 




#get their total spotify streams 

#get top 10 songs
def top_ten_songs(top10_artists):
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="YOUR_APP_CLIENT_ID",
                                            client_secret="YOUR_APP_CLIENT_SECRET",
                                            redirect_uri="YOUR_APP_REDIRECT_URI",
                                            scope="user-library-read"))
    top10_songs = []
    for artist in top10_artists:
        response = sp.artist_top_tracks(artist)
        for track in response['tracks']:
            song_names = track['name']
            top10_songs.append(song_names)
    all_top_songs = top10_songs[:100]

    print(all_top_songs)


def main():
    top_artists = parse_web_with_soup("https://chartmasters.org/most-streamed-artists-ever-on-spotify/")
    top_ten_songs(top_artists)


if __name__ == '__main__':
    main()


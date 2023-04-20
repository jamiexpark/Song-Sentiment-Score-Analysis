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
from lyricsgenius import Genius
# from transformers import pipeline
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# import torch
import requests

conn = sqlite3.connect('music.db')

c = conn.cursor()

# c.execute("""CREATE TABLE IF NOT EXISTS artists(
#             name TEXT,
#             streams TEXT,
#             UNIQUE(name, streams)
#             )""")

c.execute('''CREATE TABLE IF NOT EXISTS songs 
             (artist TEXT, song1 TEXT, song2 TEXT, song3 TEXT, song4 TEXT, song5 TEXT, 
             song6 TEXT, song7 TEXT, song8 TEXT, song9 TEXT, song10 TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS top_songs
             (artist_id INTEGER, song TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS related_artists
             (id INTEGER PRIMARY KEY, artist TEXT, related_artist TEXT)''')



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
    # counter = 0
    # for row in rows :
    #   if counter == 10:
    #     break
    #   cols = row.find_all('td')
    #   artist = cols[2].contents
    #   artist = artist[0].contents
    #   artist = artist[0].contents
   
    #   streams = cols[3].text.strip()
    #   artist_streams.append((artist, streams))
    #   counter += 1
    counter = 0
    for row in rows :
      if counter == 100:
        break
      cols = row.find_all('td')
      artist = cols[2].contents
      artist = artist[0]
      artist = str(artist)

      regex_pattern_1 = r'<b>(.*?)<\/b>'
      regex_pattern_2 = r'<a[^>]*>(.*?)<\/a>'

      match_1 = re.search(regex_pattern_1, artist)
      if match_1:
        artist = match_1.group(1)

      match_2 = re.search(regex_pattern_2, artist)
      if match_2:
        artist = match_2.group(1)


      streams = cols[3].text.strip()
      artist_streams.append((artist, streams))
      counter += 1
      
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS artists(
            name TEXT,
            streams TEXT,
            UNIQUE(name, streams)
            )""")
    c.executemany("INSERT OR IGNORE INTO artists VALUES (?, ?)", artist_streams)
    conn.commit()
    # conn.close()

    return artist_streams



#read in the soup 




#read the website (chartmasters)



#get top 10 artists 

#get top 10 songs
def top_ten_songs(artist_streams):
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id='298e33767b2644d58fe23abb08548375',
                                                           client_secret='d71c51c82f9d4320b29b9625e5a83f77'))
    
    top10_artists = artist_streams[:10]
    names_only = []
    for item in top10_artists:
        name = item[0]
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

    for artist_name, title in top10_by_artist:
        c.execute("INSERT INTO songs (artist, song1, song2, song3, song4, song5, song6, song7, song8, song9, song10) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (artist_name, *title))
        
    for i, (name_artist, song_title) in enumerate(top10_by_artist, start=1):
        for song in song_title:
            c.execute("INSERT INTO top_songs (artist_id, song) VALUES (?, ?)", (i, song))


    return top10_by_artist

def related_artists(artist_streams):
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id='298e33767b2644d58fe23abb08548375',
                                                           client_secret='d71c51c82f9d4320b29b9625e5a83f77'))
    
    top10_artists = artist_streams[:10]
    names_only = []
    for item in top10_artists:
        name = item[0]
        names_only.append((name))

    list_artist = ('3TVXtAsR1Inumwj472S9r4','4q3ewBCX7sLwd24euuV69X','06HL4z0CvFAxyc27GXpf02','6eUKZXaKkcviH0Ku9w2n3V','1Xyo4u8uXC1ZmMpatF05PJ','1uNFoZAHBGtllmzznpCI3s','66CXWjxzNUsdJxJ2JdwvnR','7dGJo4pcD2V6oG8kP0tJRR','3Nrfpe0tUJi4K4DXYWgMUX','246dkjvS1zLTtiykXe5h60')
 
 #related artists
    r = []
    for artist_name in list_artist:
        re = sp.artist_related_artists(artist_name)
        for name in re['artists'][:20]:
            artist = name['name']
            r.append(artist)

    related_per_artist = []
    for i in range(0, len(r), 20):
        group = r[i:i + 20]
        related_per_artist.append(tuple(group))

    top_related = []
    for i in range(len(names_only)):
        top_related.append((names_only[i], related_per_artist[i]))

    for artist_id, (artist, related) in enumerate(top_related, start=1):
        for name_artist in related:
            c.execute("INSERT INTO related_artists (artist_id, artist, related_artist) VALUES (?, ?, ?)",
                    (artist_id, artist, name_artist))
    
    conn.commit()
    conn.close()

    return top_related


# c.execute("""CREATE TABLE IF NOT EXISTS sentiments(
#             song TEXT,
#             sentiment_score TEXT
#             )""")

def top_song_verses(top_10_songs):
    api_key = "DtKTvEx0TjZXb3MJt0DIY_6HmKi-jSrCMuYngYO1LJpk0UTlGdOGBgjiEokMruJz"
    genius = Genius(api_key, skip_non_songs=True, remove_section_headers=True)
    genius.timeout = 120

    # sentiment_pipeline = pipeline("sentiment-analysis")
    sentiment = SentimentIntensityAnalyzer()

    # artist = genius.search_artist("Drake", max_songs=0)
    # song123 = genius.search_song("WAIT FOR U", artist.name)
    # print(song123.lyrics)


    # artist.add_song(song)
    # artist.add_song("Rich Flex")
    # artist.save_lyrics()

    # print(songs)
    # song = artist.song("Rich Flex")
    # print(song.lyrics)
    drake_list = []
    bad_bunny_list = []
    taylor_swift_list = []
    the_weeknd_list = []
    ed_sheeran_list = []
    justin_bieber_list = []
    ariana_grande_list = []
    eminem_list = []
    bts_list = []
    post_malone_list = []


    index = 1
    pattern = r'^(.*?)(\s*(\(|\[|\-).*)?$'
    # pattern = r'^([\w\s]+)(?:(?:\s-\s)|(?:\s\(|\[))(?:.*)'
    for artist, songs in top_10_songs:
        for song in songs:
            if song == "Anti-Hero":
                taylor_swift_list.append(song)
                index += 1
            match = re.match(pattern, song)
            if match:
                # print(match.group(1))
                if index <= 10:
                    drake_list.append(match.group(1))
                elif index > 10 and index <= 20:
                    bad_bunny_list.append(match.group(1))
                elif index > 20 and index <= 30:
                    if match.group(1) == "Anti":
                        continue
                    taylor_swift_list.append(match.group(1))
                elif index > 30 and index <= 40:
                    the_weeknd_list.append(match.group(1))
                elif index > 40 and index <= 50:
                    ed_sheeran_list.append(match.group(1))
                elif index > 50 and index <= 60:
                    justin_bieber_list.append(match.group(1))
                elif index > 60 and index <= 70:
                    ariana_grande_list.append(match.group(1))
                elif index > 70 and index <= 80:
                    eminem_list.append(match.group(1))
                elif index > 80 and index <= 90:
                    bts_list.append(match.group(1))
                elif index > 90 and index <= 100:
                    post_malone_list.append(match.group(1))
            index += 1
    # print(drake_list)
    # print(bad_bunny_list)
    # print(taylor_swift_list)
    # print(the_weeknd_list)
    # print(ed_sheeran_list)
    # print(justin_bieber_list)
    # print(ariana_grande_list)
    # print(eminem_list)
    # print(bts_list)
    # print(post_malone_list)
    drake_lyric_list = []
    bad_bunny_lyric_list = []
    taylor_swift_lyric_list = []
    the_weeknd_lyric_list = []
    ed_sheeran_lyric_list = []
    justin_bieber_lyric_list = []
    ariana_grande_lyric_list = []
    eminem_lyric_list = []
    bts_lyric_list = []
    post_malone_lyric_list = []
    # print(drake_lyric_list)
    for song in drake_list:
        artist = genius.search_artist("Drake", max_songs=0)
        song1 = genius.search_song(song, artist.name)
        lyrics = song1.lyrics
        # clean_lyrics = re.sub(r'^.*?(?=\n\n)|\\n|Translations.*$|\d+', '', lyrics, flags=re.DOTALL)
        clean_lyrics = lyrics.replace("\n", " ")
        clean_lyrics = clean_lyrics.replace("Embed", "")
        clean_lyrics = clean_lyrics.replace("\\", "")
        drake_lyric_list.append(clean_lyrics)
    
    print(drake_lyric_list)
    # for song in bad_bunny_list:
    #     artist = genius.search_artist("Bad Bunny", max_songs=0)
    #     song1 = genius.search_song(song, artist.name)
    #     bad_bunny_lyric_list.append(song1.lyrics)

    # for song in taylor_swift_list:
    #     artist = genius.search_artist("Taylor Swift", max_songs=0)
    #     song1 = genius.search_song(song, artist.name)
    #     taylor_swift_lyric_list.append(song1.lyrics)

    # for song in the_weeknd_list:
    #     artist = genius.search_artist("The Weeknd", max_songs=0)
    #     song1 = genius.search_song(song, artist.name)
    #     the_weeknd_lyric_list.append(song1.lyrics)

    # for song in ed_sheeran_list:
    #     artist = genius.search_artist("Ed Sheeran", max_songs=0)
    #     song1 = genius.search_song(song, artist.name)
    #     ed_sheeran_lyric_list.append(song1.lyrics)

    # for song in justin_bieber_list:
    #     artist = genius.search_artist("Justin Bieber", max_songs=0)
    #     song1 = genius.search_song(song, artist.name)
    #     justin_bieber_lyric_list.append(song1.lyrics)

    # for song in ariana_grande_list:
    #     artist = genius.search_artist("Ariana Grande", max_songs=0)
    #     song1 = genius.search_song(song, artist.name)
    #     ariana_grande_lyric_list.append(song1.lyrics)

    # for song in eminem_list:
    #     artist = genius.search_artist("Eminem", max_songs=0)
    #     song1 = genius.search_song(song, artist.name)
    #     eminem_lyric_list.append(song1.lyrics)

    # for song in bts_list:
    #     artist = genius.search_artist("BTS", max_songs=0)
    #     song1 = genius.search_song(song, artist.name)
    #     bts_lyric_list.append(song1.lyrics)

    # for song in post_malone_list:
    #     artist = genius.search_artist("Post Malone", max_songs=0)
    #     song1 = genius.search_song(song, artist.name)
    #     post_malone_lyric_list.append(song1.lyrics)
   
    # print(sentiment_pipeline(drake_lyric_list))
    # sentiment_pipeline(drake_lyric_list)
    drake_sent = []
    for drake_song in drake_lyric_list:
        sents = sentiment.polarity_scores(drake_song)
        drake_sent.append(sents['compound'])
    drake_tups = list(zip(drake_list, drake_sent))
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS sentiments(
            song TEXT,
            sentiment_score TEXT
            )""")
    c.executemany("INSERT INTO sentiments VALUES (?, ?)", drake_tups)


    conn.commit()
    # print(drake_lyric_list)

    
  #artist name vs number of streams bargraph 
    c = conn.cursor()


    c.execute("SELECT name, streams FROM artists")
    data = c.fetchall()
    artists = []
    streams = []
    for row in data[:15]:
      artists.append(row[0])
      streams.append(int(row[1].replace(',', ''))) 

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(artists, streams)

    ax.set_xlabel('Artist Name')
    ax.set_ylabel('Streams')
    ax.set_title('Top Artists by Streams')

    plt.xticks(rotation=45, ha='right')
    plt.show()
    conn.close()


def main():
    top_artists = parse_web_with_soup("https://chartmasters.org/most-streamed-artists-ever-on-spotify/")
    # print(top_artists)
    # top_artists
    top_songs = top_ten_songs(top_artists)
    top_song_verses(top_songs)
    # print(top_songs)




if __name__ == '__main__':
    main()


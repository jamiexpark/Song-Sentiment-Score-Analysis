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
    list_artist = ('3TVXtAsR1Inumwj472S9r4','4q3ewBCX7sLwd24euuV69X','06HL4z0CvFAxyc27GXpf02','1Xyo4u8uXC1ZmMpatF05PJ', '6eUKZXaKkcviH0Ku9w2n3V', '1uNFoZAHBGtllmzznpCI3s','66CXWjxzNUsdJxJ2JdwvnR','7dGJo4pcD2V6oG8kP0tJRR','3Nrfpe0tUJi4K4DXYWgMUX','246dkjvS1zLTtiykXe5h60')

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

def top_song_verses(top_10_songs):
    api_key = "DtKTvEx0TjZXb3MJt0DIY_6HmKi-jSrCMuYngYO1LJpk0UTlGdOGBgjiEokMruJz"
    genius = Genius(api_key, skip_non_songs=True, remove_section_headers=True)
    genius.timeout = 120

    sentiment = SentimentIntensityAnalyzer()

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

    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS sentiments(
            song TEXT,
            sentiment_score TEXT
            )""")
    
    c.execute("SELECT COUNT(*) FROM sentiments")
    row_count = c.fetchone()[0]
    print(row_count)
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

    drake_sent = []
    bad_sent = []
    tay_sent = []
    week_sent = []
    ed_sent = []
    justin_sent = []
    ariana_sent = []
    em_sent = []
    bts_sent = []
    post_sent = []

    if row_count == 100:
        return
    else:
        if row_count == 0:
            for song in drake_list:
                artist = genius.search_artist("Drake", max_songs=0)
                song1 = genius.search_song(song, artist.name)
                lyrics = song1.lyrics
                clean_lyrics = lyrics.replace("\n", " ")
                clean_lyrics = clean_lyrics.replace("Embed", "")
                clean_lyrics = clean_lyrics.replace("\\", "")
                drake_lyric_list.append(clean_lyrics)

            for drake_song in drake_lyric_list:
                sents = sentiment.polarity_scores(drake_song)
                drake_sent.append(sents['compound'])

            drake_tups = list(zip(drake_list, drake_sent))
            c.executemany("INSERT INTO sentiments VALUES (?, ?)", drake_tups)
            conn.commit()

        elif row_count == 10:
            for song in bad_bunny_list:
                artist = genius.search_artist("Bad Bunny", max_songs=0)
                song1 = genius.search_song(song, artist.name)
                lyrics = song1.lyrics
                clean_lyrics = lyrics.replace("\n", " ")
                clean_lyrics = clean_lyrics.replace("Embed", "")
                clean_lyrics = clean_lyrics.replace("\\", "")
                bad_bunny_lyric_list.append(clean_lyrics)

            for bad_song in bad_bunny_lyric_list:
                sents = sentiment.polarity_scores(bad_song)
                bad_sent.append(sents['compound'])

            bad_tups = list(zip(bad_bunny_list, bad_sent))
            c.executemany("INSERT INTO sentiments VALUES (?, ?)", bad_tups)
            conn.commit()

        elif row_count == 20:
            for song in taylor_swift_list:
                artist = genius.search_artist("Taylor Swift", max_songs=0)
                song1 = genius.search_song(song, artist.name)
                lyrics = song1.lyrics
                clean_lyrics = lyrics.replace("\n", " ")
                clean_lyrics = clean_lyrics.replace("Embed", "")
                clean_lyrics = clean_lyrics.replace("\\", "")
                taylor_swift_lyric_list.append(clean_lyrics)
            
            for tay_song in taylor_swift_lyric_list:
                sents = sentiment.polarity_scores(tay_song)
                tay_sent.append(sents['compound'])

            tay_tups = list(zip(taylor_swift_list, tay_sent))
            c.executemany("INSERT INTO sentiments VALUES (?, ?)", tay_tups)
            conn.commit()

        elif row_count == 30:
            for song in the_weeknd_list:
                artist = genius.search_artist("The Weeknd", max_songs=0)
                song1 = genius.search_song(song, artist.name)
                lyrics = song1.lyrics
                clean_lyrics = lyrics.replace("\n", " ")
                clean_lyrics = clean_lyrics.replace("Embed", "")
                clean_lyrics = clean_lyrics.replace("\\", "")
                the_weeknd_lyric_list.append(clean_lyrics)

            for week_song in the_weeknd_lyric_list:
                sents = sentiment.polarity_scores(week_song)
                week_sent.append(sents['compound'])

            week_tups = list(zip(the_weeknd_list, week_sent))
            c.executemany("INSERT INTO sentiments VALUES (?, ?)", week_tups)
            conn.commit()

        elif row_count == 40:
            for song in ed_sheeran_list:
                artist = genius.search_artist("Ed Sheeran", max_songs=0)
                song1 = genius.search_song(song, artist.name)
                lyrics = song1.lyrics
                clean_lyrics = lyrics.replace("\n", " ")
                clean_lyrics = clean_lyrics.replace("Embed", "")
                clean_lyrics = clean_lyrics.replace("\\", "")
                ed_sheeran_lyric_list.append(clean_lyrics)

            for ed_song in ed_sheeran_lyric_list:
                sents = sentiment.polarity_scores(ed_song)
                ed_sent.append(sents['compound'])

            ed_tups = list(zip(ed_sheeran_list, ed_sent))
            c.executemany("INSERT INTO sentiments VALUES (?, ?)", ed_tups)
            conn.commit()

        elif row_count == 50:
            for song in justin_bieber_list:
                artist = genius.search_artist("Justin Bieber", max_songs=0)
                song1 = genius.search_song(song, artist.name)
                lyrics = song1.lyrics
                clean_lyrics = lyrics.replace("\n", " ")
                clean_lyrics = clean_lyrics.replace("Embed", "")
                clean_lyrics = clean_lyrics.replace("\\", "")
                justin_bieber_lyric_list.append(song1.lyrics)

            for justin_song in justin_bieber_lyric_list:
                sents = sentiment.polarity_scores(justin_song)
                justin_sent.append(sents['compound'])

            justin_tups = list(zip(justin_bieber_list, justin_sent))
            c.executemany("INSERT INTO sentiments VALUES (?, ?)", justin_tups)
            conn.commit()
                
        elif row_count == 60:
            for song in ariana_grande_list:
                artist = genius.search_artist("Ariana Grande", max_songs=0)
                song1 = genius.search_song(song, artist.name)
                lyrics = song1.lyrics
                clean_lyrics = lyrics.replace("\n", " ")
                clean_lyrics = clean_lyrics.replace("Embed", "")
                clean_lyrics = clean_lyrics.replace("\\", "")
                ariana_grande_lyric_list.append(clean_lyrics)

            for ariana_song in ariana_grande_lyric_list:
                sents = sentiment.polarity_scores(ariana_song)
                ariana_sent.append(sents['compound'])

            ariana_tups = list(zip(ariana_grande_list, ariana_sent))
            c.executemany("INSERT INTO sentiments VALUES (?, ?)", ariana_tups)
            conn.commit()

        elif row_count == 70:
            for song in eminem_list:
                artist = genius.search_artist("Eminem", max_songs=0)
                song1 = genius.search_song(song, artist.name)
                lyrics = song1.lyrics
                clean_lyrics = lyrics.replace("\n", " ")
                clean_lyrics = clean_lyrics.replace("Embed", "")
                clean_lyrics = clean_lyrics.replace("\\", "")
                eminem_lyric_list.append(clean_lyrics)

            for em_song in eminem_lyric_list:
                sents = sentiment.polarity_scores(em_song)
                em_sent.append(sents['compound'])

            em_tups = list(zip(eminem_list, em_sent))
            c.executemany("INSERT INTO sentiments VALUES (?, ?)", em_tups)
            conn.commit()

        elif row_count == 80:
            for song in bts_list:
                artist = genius.search_artist("BTS", max_songs=0)
                song1 = genius.search_song(song, artist.name)
                lyrics = song1.lyrics
                clean_lyrics = lyrics.replace("\n", " ")
                clean_lyrics = clean_lyrics.replace("Embed", "")
                clean_lyrics = clean_lyrics.replace("\\", "")
                bts_lyric_list.append(song1.lyrics)

            for bts_song in bts_lyric_list:
                sents = sentiment.polarity_scores(bts_song)
                bts_sent.append(sents['compound'])

            bts_tups = list(zip(bts_list, bts_sent))
            c.executemany("INSERT INTO sentiments VALUES (?, ?)", bts_tups)
            conn.commit()

        elif row_count == 90:
            for song in post_malone_list:
                artist = genius.search_artist("Post Malone", max_songs=0)
                song1 = genius.search_song(song, artist.name)
                lyrics = song1.lyrics
                clean_lyrics = lyrics.replace("\n", " ")
                clean_lyrics = clean_lyrics.replace("Embed", "")
                clean_lyrics = clean_lyrics.replace("\\", "")
                post_malone_lyric_list.append(clean_lyrics)

            for post_song in post_malone_lyric_list:
                sents = sentiment.polarity_scores(post_song)
                post_sent.append(sents['compound'])

            post_tups = list(zip(post_malone_list, post_sent))
            c.executemany("INSERT INTO sentiments VALUES (?, ?)", post_tups)
            conn.commit()

    conn.close()

def main():
    top_artists = parse_web_with_soup("https://chartmasters.org/most-streamed-artists-ever-on-spotify/")
    # print(top_artists)
    # top_artists
    top_songs = top_ten_songs(top_artists)
    # print(top_songs)
    top_song_verses(top_songs)
    # print(top_songs)




if __name__ == '__main__':
    main()


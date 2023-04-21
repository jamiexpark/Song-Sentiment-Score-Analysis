import numpy as np
import seaborn as sns
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
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import requests

def my_func():
    print("Hello from B")

#visualization 1
#artist name vs number of streams bargraph 
def visualizations(conn):
    visual_one(conn)
    visual_two(conn)
    # visual_three(conn)

def visual_one(conn):
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
    sns.color_palette('pastel')

    plt.xticks(rotation=45, ha='right')
    plt.show()
    #visualization2 sentiment score average




def visual_two(conn):
    c = conn.cursor()

    c.execute("SELECT sentiment_score FROM sentiments")
    sentiment_scores = c.fetchall()

    sentiment_scores = [float(score[0]) for score in sentiment_scores]

    avg_sentiment_scores = []
    count = 0
    total = 0
    for score in sentiment_scores:
        total += score
        count += 1
        if count == 10:
            avg_sentiment_scores.append(total/10)
            total = 0
            count = 0

    c.execute("SELECT name FROM artists LIMIT 10")
    artist_names = c.fetchall()
    meow = 1
 
    artist_names = [name[0] for name in artist_names]

    fig, ax = plt.subplots()
    ax.bar(artist_names, avg_sentiment_scores)  
    ax.set_xlabel('Song')
    ax.set_ylabel('Average Sentiment Score')
    ax.set_title('Average Sentiment Scores for Every 10 Songs')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()
    conn.close()



def visual_three(conn):
    print("visual3")


def visual_test(conn):
    c = conn.cursor()
    c.execute("SELECT song, sentiment_score FROM sentiments")
    data = c.fetchall()

    v_song = []
    v_sentiment_score = []
    for row in data:
        v_song.append(row[0])
        v_sentiment_score.append(float(row[1]))

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(v_song, v_sentiment_score)

    ax.set_xlabel('Song')
    ax.set_ylabel('Sentiment Scores')
    ax.set_title('Drake\'s Songs vs. Sentiment Score')

    plt.xticks(rotation=45, ha='right')
    plt.show()

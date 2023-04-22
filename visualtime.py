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
    visual_three(conn)

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
    artist_names = [name[0] for name in artist_names]
    # avg_scores = [score[1] for score in avg_sentiment_scores]


    fig, ax = plt.subplots()
    ax.bar(artist_names, avg_sentiment_scores)  
    ax.set_xlabel('Song')
    ax.set_ylabel('Average Sentiment Score')
    ax.set_title('Average Sentiment Scores for Every 10 Songs')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def visual_three(conn):
    print("visual3")
    c = conn.cursor()

    c.execute("SELECT DISTINCT song, sentiment_score FROM sentiments ORDER BY sentiment_score DESC LIMIT 10")
    top_songs = c.fetchall()
    top_song_names = [row[0] for row in top_songs]
    top_sentiment_scores = [float(row[1]) for row in top_songs]

    c.execute("SELECT DISTINCT song, sentiment_score FROM sentiments ORDER BY sentiment_score ASC LIMIT 10")
    bottom_songs = c.fetchall()
    bottom_song_names = [row[0] for row in bottom_songs]
    bottom_sentiment_scores = [float(row[1]) for row in bottom_songs]
   
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))


    ax1.set_xlabel('Songs with Highest Sentiment Scores')
    ax1.set_ylabel('Sentiment Score')
    ax1.set_ylim([0.9, 1.1])
    ax1.set_yticks([0.9, 0.95, 1])  
    ax1.set_yticklabels([0.9, 0.95, 1]) 
    ax1.bar(top_song_names, top_sentiment_scores)
   
    ax2.set_xlabel('Songs with Lowest Sentiment Scores')
    ax2.set_ylabel('Sentiment Score')
    ax2.set_ylim([-1.1, 1.1]) 
    ax2.set_yticks([-1, -0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75, 1]) 
    ax2.set_yticklabels([-1, -0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75, 1])  
    ax2.bar(bottom_song_names, bottom_sentiment_scores)

    fig.suptitle('Sentiment Scores for Songs with Highest and Lowest Sentiment Scores')

    plt.subplots_adjust(wspace=0.3)
    plt.show()

    conn.close()


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

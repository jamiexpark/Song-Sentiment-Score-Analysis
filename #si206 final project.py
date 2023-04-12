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


#beautiful soup portion 
def parse_web_with_soup(website):
    try:
        with open(website, 'r', encoding='utf-8-sig') as f:
            soup = BeautifulSoup(f, 'html.parser')
    except FileNotFoundError:
        print(f"Error: could not open file {website}")
        return []

    data = []

#read in the soup 




#read the website (chartmasters)



#get top 10 artists 



#get their total spotify streams 


class TestCases(unittest.TestCase):
    def test_parse_web_with_soup(self):
        print("tets")

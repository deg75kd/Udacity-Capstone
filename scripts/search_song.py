import pandas as pd
import numpy as np
import requests
import xml.etree.ElementTree as ET
import urllib

from urllib.request import urlopen
from sklearn.externals import joblib

from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from scripts.myfunctions import tokenize

def search_song(song_name):
    """Use ChartLyrics API to find song matches

    Args:
        song_name (string): song name to search for

    Returns:
        song_df (dataframe): details of matching songs
    """
    base_url = 'http://api.chartlyrics.com/apiv1.asmx/SearchLyricText?'
    qs_args = {'lyricText': song_name}
    search_url = base_url + urllib.parse.urlencode(qs_args)
    print(search_url)

    response = urllib.request.urlopen(search_url)
    content = response.read().decode('ascii')
    data = ET.fromstring(content)

    song_df = pd.DataFrame(columns = ['lyric_id', 'lyric_check_sum', 'artist', 'song'])

    for item in data.iterfind('*'):
        artist = item.findtext('{http://api.chartlyrics.com/}Artist')
        song = item.findtext('{http://api.chartlyrics.com/}Song')
        lyric_id = item.findtext('{http://api.chartlyrics.com/}LyricId')
        lyric_cs = item.findtext('{http://api.chartlyrics.com/}LyricChecksum')
    
        song_df = song_df.append({'lyric_id': lyric_id, 
                                  'lyric_check_sum': lyric_cs, 
                                  'artist': artist, 
                                  'song': song}, 
                                  ignore_index=True)

    song_df = song_df.dropna(axis=0)
    result_count = song_df.shape[0]

    # limit results to 10
    if result_count > 10:
        song_df = song_df.head(10)

    return song_df
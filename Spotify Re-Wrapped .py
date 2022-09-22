#!/usr/bin/env python
# coding: utf-8

# In[1]:


from spotipy import Spotify as sp
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import time
import datetime


# In[2]:


SPOTIPY_CLIENT_ID='#enter your client num'
SPOTIPY_CLIENT_SECRET='#enter your client secret num'
SPOTIPY_REDIRECT_URI='http://localhost/'
SCOPE = "user-top-read"


# In[3]:


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, 
                                               client_secret=SPOTIPY_CLIENT_SECRET, 
                                               redirect_uri=SPOTIPY_REDIRECT_URI, 
                                               scope=SCOPE))


# In[4]:


top_tracks_short = sp.current_user_top_tracks(limit=10, offset=0, time_range="short_term")


# In[5]:


top_tracks_short


# In[6]:


top_tracks_short = sp.current_user_top_tracks(limit=20, offset=0, time_range="short_term")


# In[7]:


type(top_tracks_short)


# In[8]:


def get_track_ids(time_frame):
    track_ids = []
    for song in time_frame['items']:
        track_ids.append(song['id'])
    return track_ids


# In[9]:


track_ids = get_track_ids(top_tracks_short)


# In[10]:


track_ids


# In[11]:


track_id ='6rlQYRWG6ZN5X89LA0zBE7'


# In[12]:


def get_track_features(id):
    meta= sp.track(id)
    name = meta['name']
    album = meta['album']['name']
    artist = meta['album']['artists'][0]['name']
    spotify_url = meta ['external_urls']['spotify']
    album_cover = meta ['album']['images'][0]['url']
    track_info = [name, album, artist, spotify_url, album_cover]
    return track_info


# In[13]:


get_track_features(track_id)


# In[14]:


#Loop fxn
tracks = []
for i in range(len(track_ids)):
    time.sleep(.5)
    track=get_track_features(track_ids[i])
    tracks.append(track)


# In[15]:


tracks


# In[16]:


dataset = pd.DataFrame(tracks, columns = ['name', 'album', 'artist', 'spotify_url','album_cover'])
dataset.head(5)


# In[17]:


import gspread


# In[18]:


gc = gspread.service_account(filename='#enter pathway for json file')


# In[19]:


sh = gc.open_by_url("#enter link to google spreadsheet")


# In[20]:


worksheet = sh.worksheet("short_term")


# In[21]:


#worksheet.update([dataframe.columns.values.tolist() + dataframe.values.tolist()])


# In[22]:


def insert_gsheet(track_ids):
    tracks = []
    for i in range(len(track_ids)):
        time.sleep(.5)
        track = get_track_features(track_ids[i])
        tracks.append(track)
    df = pd.DataFrame(tracks, columns = ['name', 'album', 'artist', 'spotify_url', 'album_cover'])
    
    gc = gspread.service_account(filename = '#enter json file again')
    sh = gc.open_by_url("#enter google sheet url")
    worksheet = sh.worksheet(f'{time_period}')
    worksheet.update([df.columns.values.tolist()] +df.values.tolist())
    print('Done')


# In[23]:


time_ranges = ['short_term', 'medium_term', 'long_term']
for time_period in time_ranges: 
    top_tracks = sp.current_user_top_tracks(limit=20, offset=0, time_range=time_period)
    track_ids = get_track_ids(top_tracks)
    insert_gsheet(track_ids)


# In[ ]:





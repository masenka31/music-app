import os
import pandas as pd
import random

def read_data():
    data = pd.read_csv('data/song_info_v1.4.csv', usecols=["track_id", "track_name", "artist_name"])
    return data

def find_artist(name, data,n):
    yon = data['artist_name'].str.contains(name).sum()
    rand_sample = data.sample(n)
    return yon, rand_sample

def artists_list(data):
    artists = data.artist_name.unique()
    return artists

def song_list(data,art_name):
    songList = data.loc[data['artist_name'] == art_name ]
    return songList['track_name']

def song_list2(data,art_name):
    songList_temp = data.loc[data['artist_name'] == art_name ]
    songNames = songList_temp['track_name']
    songIDs = songList_temp['track_id']
    return zip(songNames, songIDs)

def names_from_ids(data,ids):
    song_names = data.loc[data['track_id'].isin(ids)]
    return song_names['track_name']

def idtonames(data,ids):
    songs = data.loc[data['track_id'].isin(ids)]
    tmp = pd.DataFrame({'tmp': ids})
    df = tmp.merge(songs, left_on='tmp', right_on='track_id')
    song_names = df['track_name'].tolist()
    artists = df['artist_name'].tolist()
    return song_names, artists

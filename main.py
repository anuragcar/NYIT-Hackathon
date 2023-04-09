from re import search
import spotipy
import sys
from spotipy.oauth2 import SpotifyClientCredentials
from pytube import Search
# from google.cloud import language_v1
# import six
import requests
import json
from flask import Flask, render_template
import cherrypy

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id='',client_secret='',))
# get spotify uri
def getSpotify(mood):
    results = spotify.search(q=mood, type='playlist')
    if results['playlists']['total'] > 0:
        track_uri = results['playlists']['items'][0]['uri']
        print(track_uri)
        with open('spotify.txt', 'w') as f:
            f.write(track_uri)
        return track_uri
    else:
        return None

def getYouTube(mood):
    s = Search(f"{mood} songs")
    video_url = 'https://www.youtube.com/watch?v='
    t = (str)(s.results[0])
    video_url += (t[t.index('videoId=')+8:-1])
    description_string = (video_url)
    print(video_url)
    with open('youtube.txt', 'w') as f:
        f.write(video_url)

def aiAPI(inp):
    url = "https://emodex-emotions-analysis.p.rapidapi.com/rapidapi/emotions"

    payload = {"sentence": inp}
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "fdf37857e7msh4f6ba154cd26974p107aefjsne430cd0fd394",
        "X-RapidAPI-Host": "emodex-emotions-analysis.p.rapidapi.com"
    }

    results = requests.request("POST", url, json=payload, headers=headers)
    response = json.loads(results.content)
    emotions = []

    emotions.append(float(response['sentence']['anger']))
    emotions.append(float(response['sentence']['disgust'])) 
    emotions.append(float(response['sentence']['fear'])) 
    emotions.append(float(response['sentence']['joy']))
    emotions.append(float(response['sentence']['love']))
    emotions.append(float(response['sentence']['noemo']))
    emotions.append(float(response['sentence']['sadness']))
    emotions.append(float(response['sentence']['surprise']))
    
    value=0
    comparison=0
    
    for i in range(0, len(emotions)):
        if emotions[i] > value:
            value = emotions[i]
            comparison = i
            
    match comparison:
        case 0:
            mood = 'anger'   
        case 1:
            mood = 'disgust'
        case 2:
            mood = 'fear'
        case 3:
            mood = 'joy'
        case 4:
            mood = 'love'
        case 5:
            mood = 'no emotions'
        case 6:
            mood = 'sad'
        case 7:
            mood = 'surprise'
            
    getSpotify(mood)
    getYouTube(mood)
    # print(results.text)
    # print(emotions)

while True: 
    inp = input('How are you?')
    aiAPI(inp)


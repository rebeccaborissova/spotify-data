from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json

load_dotenv()

client_id = "5af2558b2210451aba54d8e7b892243e"
client_secret = "ae72dc09479540558d120aa6b8d7da1d"

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"q={artist_name}&type=artist&limit=1"

    query_url = url + "?" +query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    
    if len(json_result) == 0:
        print("No artists with this name exists...")
        return None
    
    return json_result[0]

def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result

def get_songs_by_genre(token, genre):
    url=f"https://api.spotify.com/v1/search?q=genre%3A{genre}&type=track&market=US&limit=50"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]["items"]
    return json_result

def get_all_songs(token):
    house_songs = get_songs_by_genre(token, "house")
    techno_songs = get_songs_by_genre(token, "techno")
    edm_songs = get_songs_by_genre(token, "edm")
    tech_house_songs = get_songs_by_genre(token, "tech house")
    dubstep_songs = get_songs_by_genre(token, "dubstep")
    dnb_songs = get_songs_by_genre(token, "drum and bass")
    return house_songs + techno_songs + edm_songs + tech_house_songs + dubstep_songs + dnb_songs


token = get_token()
songs = get_all_songs(token)


num = 1
for genre_song in songs:
    print(num, ".")
    print(genre_song['name'], "-", genre_song['artists'][0]['name'])
    print()
    num += 1



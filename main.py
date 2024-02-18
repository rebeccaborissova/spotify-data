from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# authenticates client keys and returns access token
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
    
# takes access token and creates authentication header
def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

# searches for artists by name
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

# returns artist's top tracks in the US
def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result
    
# pulls songs from spotify by genre 
def get_songs_by_genre(token, genre):
    url=f"https://api.spotify.com/v1/search?q=genre%3A{genre}&type=track&market=US&limit=50"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]["items"]
    return json_result

def get_popularity(song):
    return song['popularity']


# example of songs by ACDC
token = get_token()
result = search_for_artist(token, "ACDC")
artist_id = result["id"]
songs = get_songs_by_artist(token, artist_id)
print(songs)

for idx, song in enumerate(songs):
    print(f"{idx + 1}.{song['name']}")

# example of songs by 'house' genre
genre_songs = get_songs_by_genre(token, "house")
print(genre_songs)

for genre_song in genre_songs:
    print(genre_song['name'])
    
# example of top 10 
sorted_house = sorted(genre_songs, key=get_popularity, reverse=True) # sorted in descending order
house_top_10 = sorted_house[:10]
print("Top 10 House Songs in the U.S")
for idx, song in enumerate(house_top_10):
    print(f"{idx + 1}. {song['name']} by {', '.join(artist['name'] for artist in song['artists'])}")
 
 # example of bottom 10 
sorted_house = sorted(genre_songs, key=get_popularity) # sorted in ascending order
house_bottom_10 = sorted_house[:10]
print("Bottom 10 House Songs in the U.S")
for idx, song in enumerate(house_bottom_10):
    print(f"{idx + 1}. {song['name']} by {', '.join(artist['name'] for artist in song['artists'])}")
 


import requests
import os
import json
from secret import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
class spotify_api:
    def __init__(self):
        self.token = self.get_token()

    def get_token(self):
        token_url = "https://accounts.spotify.com/api/token"
        token_data = {
        "grant_type": "client_credentials",
        "client_id": SPOTIFY_CLIENT_ID,
        "client_secret": SPOTIFY_CLIENT_SECRET
        }
        token_response = requests.post(token_url, data=token_data)
        #The response of spotify api is the following. Spotify api is more strict than other. We need to get an access token in order to use the api.
        #The token lasts 1 hour.
        ##JSON RESPONSE:
        #{
        #    "access_token":"BQCffR2r0vAIRXz5BCEIy5fdA6YvapFGomSxLMcJ8DIci99Qhx04vTQBVy5X656yK34HnbIB0NvJ2hW7EDf0I06xvQBa7haCcEEseysCyRN-G1Yb5Yw",
        #    "token_type":"Bearer",
        #    "expires_in":3600
        #}
        #token = token_response.json().get("access_token")
        token = token_response.json()["access_token"]
        #print(token_response.json())
        #print(token)
        return token
    
    def get_track_info(self, id):
        header = {
            "Authorization": f"Bearer {self.token}"
        }
        url = f"https://api.spotify.com/v1/tracks/{id}"
        response = requests.get(url, headers=header).json()
        #Get the infos we need
        #album names
        artists_arr = response["artists"]
        track_name = response["name"]
        #track number in the album
        infos = {}
        infos["artists"] = artists_arr
        infos["name"] = track_name
        return infos
        

    def get_lyrics(self, artist, title):
        url = f"https://api.lyrics.ovh/v1/{artist}/{title}"
        response = requests.get(url).json()
        print(f"Lyrics of {title}:")
        lyrics = ""
        try:
            lyrics = response["lyrics"]
        except:
            lyrics = ""
        if lyrics == "":
            print("No lyrics found")
        else:
            print(lyrics)

    def choose_track(self, tracks)->int:
        for i, track in enumerate(tracks):
            string = ""
            artists_arr = track["artists"]
            artists_string = ""
            for art in artists_arr:
                artists_string += art["name"] + ", "
            album_name = track["album"]["name"]
            track_name = track["name"]
            string += f"{i}) Artists: {artists_string} Album: {album_name} Title: {track_name}"
            print(string)
        exit = False
        index = -1
        while exit == False:
            index = input("Please choose the song of your choice: ")
            if int(index) <0 or int(index) > len(tracks)-1:
                print("Please choose a valid index")
            else:
                exit = True
        return int(index)

            





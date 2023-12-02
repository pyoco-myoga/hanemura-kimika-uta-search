import json
import os

from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, db

if __name__ == "__main__":
    load_dotenv(".env")

    credential = credentials.Certificate(
        os.environ["FIREBASE_CREDENTIAL_JSON_PATH"])
    firebase_admin.initialize_app(credential, {
        "databaseURL": os.environ["FIREBASE_DATABASE_URL"],
        })

    with open("./src/songs.json") as f:
        songs = json.load(f)

    recommended_songs = []
    for artist, songs_ in songs.items():
        for i, song in enumerate(songs_):
            if "recommended" in song.keys() and song["recommended"]:
                recommended_songs.append({
                    "uuid": song["uuid"],
                    "artist": artist,
                    "name": song["name"],
                })

    with open("./src/playlists.json") as f:
        playlists = json.load(f)

    for playlist_id, playlist_filter in playlists.items():
        playlist = []
        title = playlist_filter["title"]
        description = playlist_filter["description"]
        image = playlist_filter["image"]
        for recommended in recommended_songs:
            for filter_ in playlist_filter["filters"]:
                if filter_["artist"] == recommended["artist"] and \
                        filter_["name"] == recommended["name"]:
                    playlist.append(recommended["uuid"])
                elif filter_["artist"] == "" and \
                        filter_["name"] == recommended["name"]:
                    playlist.append(recommended["uuid"])
                elif filter_["artist"] == recommended["artist"] and \
                        filter_["name"] == "":
                    playlist.append(recommended["uuid"])

        ref = db.reference(
                f"/official_playlists/{playlist_id}/")
        if len(playlist) == 0:
            print("`playlist` is empty")
            continue
        ref.set({
            "title": title,
            "description": description,
            "image": image,
            "songs": playlist,
            })


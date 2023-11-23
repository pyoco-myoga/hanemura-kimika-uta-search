import json
import os
import itertools

import firebase_admin
from algoliasearch.search_client import SearchClient
from dotenv import load_dotenv
from firebase_admin import credentials, db

if __name__ == "__main__":
    load_dotenv(".env")

    credential = credentials.Certificate(
        os.environ["FIREBASE_CREDENTIAL_JSON_PATH"])
    firebase_admin.initialize_app(credential, {
        "databaseURL": os.environ["FIREBASE_DATABASE_URL"],
        "databaseAuthVariableOverride": {
            "uid": os.environ["FIREBASE_ADMIN_UID"]
            }
        })

    ref = db.reference(f"/users/{os.environ['FIREBASE_ADMIN_UID']}/favorite")
    recommended = ref.get()

    client = SearchClient.create(
        os.environ["ALGOLIA_APP_ID"], os.environ["ALGOLIA_SECRET_KEY"])
    index = client.init_index("songs")
    with open("./src/songs.json") as f:
        songs = json.load(f)

    modified_ids = []
    for artist, songs_ in songs.items():
        for i, song in enumerate(songs_):
            if "recommended" not in songs[artist][i].keys() or \
                songs[artist][i]["recommended"] != (song["uuid"] in recommended):
                modified_ids.append(song["uuid"])
            songs[artist][i]["recommended"] = (song["uuid"] in recommended)

    with open("./src/songs.json", "w") as f:
        f.write(json.dumps(songs, ensure_ascii=False, sort_keys=True, indent=4))

    index.save_objects(itertools.chain.from_iterable([
        [
            {
                "objectID": song["uuid"],
                "artist": artist,
                "name": song["name"],
                "video": song["video"],
                "t": song["t"],
                "endt": song["endt"],
                "recommended": song["recommended"],
                "singType": song["singType"],
                "length": song["length"]
            }
            for song in songs_
            if song["uuid"] in modified_ids
        ]
        for artist, songs_ in songs.items()
    ]))

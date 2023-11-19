import os
import json
import firebase_admin
from firebase_admin import credentials, db
from algoliasearch.search_client import SearchClient
from dotenv import load_dotenv


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

    for uuid in songs["songs"].keys():
        songs["songs"][uuid]["recommended"] = (uuid in recommended)

    with open("./src/songs.json", "w") as f:
        f.write(json.dumps(songs, ensure_ascii=False, sort_keys=True, indent=4))

    index.save_objects([
        {
            "objectID": key,
            **value
        }
        for key, value in songs["songs"].items()
    ])


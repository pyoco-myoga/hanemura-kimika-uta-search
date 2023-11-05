import os
import json
from algoliasearch.search_client import SearchClient
from dotenv import load_dotenv


if __name__ == "__main__":
    load_dotenv(".env")

    client = SearchClient.create(os.environ["ALGOLIA_APP_ID"], os.environ["ALGOLIA_SECRET_KEY"])
    index = client.init_index("songs")
    with open("./src/songs.json") as f:
        songs = json.load(f)

    index.save_objects([
        {
            "objectID": key,
            **value
        }
        for key, value in songs["songs"].items()
    ])



from collections import OrderedDict
import json


if __name__ == "__main__":
    with open("../kimika-songs/src/songs.json") as f:
        previous_data_format = json.load(f)
    with open("src/songs.json") as f:
        current_format = json.load(f)

    for artist, ds in previous_data_format.items():
        for d in ds:
            if d["uuid"] not in current_format["songs"].keys():
                current_format["songs"][d["uuid"]] = {
                    "artist": artist,
                    "name": d["name"],
                    "video": d["video"],
                    "t": d["t"],
                    "endt": d["endt"],
                    "length": d["length"],
                    "singType": d["singType"]
                }

    sorted_current_format = OrderedDict()
    sorted_current_format["songs"] = OrderedDict(sorted(
        current_format["songs"].items(),
        key=lambda x: (x[1]["artist"], x[1]["name"])))
    with open("src/songs.json", "w") as f:
        f.write(
            json.dumps(
                sorted_current_format,
                ensure_ascii=False,
                sort_keys=False,
                indent=4))


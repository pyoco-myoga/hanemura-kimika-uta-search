
import json

if __name__ == "__main__":
    article = """{|class="filter sort edit"\n|~曲名|アーティスト|\n"""
    with open("./src/songs.json") as f:
        data = json.load(f)
    for artist in data:
        for song in data[artist]:
            article += f"|[[{song['name']} >>https://www.youtube.com/watch?v={song['video']}&t={song['t']}]]|{artist}|\n"

    article += "|}"
    print(article)

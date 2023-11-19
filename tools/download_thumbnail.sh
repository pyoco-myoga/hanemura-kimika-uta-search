#!/bin/bash

cat ./src/songs.json | jq ".songs[].video" | sort | uniq | xargs -I {} sh -c "wget https://img.youtube.com/vi/{}/0.jpg -P ./src/assets/thumbnail/{} && sleep 2"

ls ./src/assets/thumbnail/ | xargs -I {} convert ./src/assets/thumbnail/{}/0.jpg -crop +0+45 -crop -0-45 ./src/assets/thumbnail/{}/0.jpg

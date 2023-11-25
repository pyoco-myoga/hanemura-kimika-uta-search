#!/bin/bash

cat ./src/songs.json | jq -r ".[] | .[] | .video" | sort | uniq | while read -r video; do
  thumbnail_path="./src/assets/thumbnail/${video}/"
  if [ ! -f "${thumbnail_path}/0.jpg" ]; then
    mkdir "${thumbnail_path}"
    wget "https://img.youtube.com/vi/${video}/0.jpg" -O "${thumbnail_path}/0.jpg" && sleep 2
    convert "${thumbnail_path}/0.jpg" -crop +0+45 -crop -0-45 -resize 50% "${thumbnail_path}/0.jpg"
  else
    echo "Thumbnail for video $video already exists. Skipping..."
  fi
done


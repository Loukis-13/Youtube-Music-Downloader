#!/bin/python

import sys
import os
import requests
from pytube import Playlist


playlist = Playlist(sys.argv[1])
videos = [*playlist.videos]
album = playlist.title.removeprefix("Album - ")
artist = videos[0].author.removesuffix(" - Topic")

if not os.path.exists(album):
    os.mkdir(album)
os.chdir(album)

thumbnail = f"{album}.jpg"
with open(thumbnail, "wb") as f: 
    f.write(requests.get(videos[0].thumbnail_url).content)
os.system(f"convert '{thumbnail}' -crop 360x360+140+60 '{thumbnail}'")

album_length = len(videos)
for i, video in enumerate(playlist.videos, 1):
    for _ in range(5):
        try:
            if not os.path.exists(f"{video.title}.mp3"):
                title = video.title
                print(title)
                video.streams.get_audio_only().download(filename=title+".mp4")
                os.system(
                    f"ffmpeg -loglevel 16 \
                    -i '{title}.mp4' \
                    -i '{thumbnail}' \
                    -map 0 -map 1 \
                    -metadata title='{title}' \
                    -metadata artist='{artist}' \
                    -metadata album='{album}' \
                    -metadata track='{i}/{album_length}' \
                    '{title}.mp3'")
                os.system(f"rm '{title}.mp4'")
            break
        except:
            pass


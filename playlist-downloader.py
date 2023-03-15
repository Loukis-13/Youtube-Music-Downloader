#!/bin/python

import sys
import os
import requests
from subprocess import run
from pytube import Playlist, exceptions


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
run(["convert", thumbnail, "-crop", "360x360+140+60", thumbnail])

album_length = len(videos)
for i, video in enumerate(playlist.videos, 1):
    if not os.path.exists(f"{video.title}.mp3"):
        for _ in range(3):
            try:
                if video.age_restricted and not video.use_oauth:
                    video.use_oauth = True

                title = video.title
                print(title)
                video.streams.get_audio_only().download(filename=f"{title}.mp4")
                run([
                    "ffmpeg", "-loglevel", "16",
                    "-i", f"{title}.mp4",
                    "-i", thumbnail,
                    "-map", "0", "-map", "1",
                    "-metadata", f"title='{title}'",
                    "-metadata", f"artist='{artist}'",
                    "-metadata", f"album='{album}'",
                    "-metadata", f"track='{i}/{album_length}'",
                    f"{title}.mp3"
                ])
                run(["rm", f"{title}.mp4"])
                break
            except exceptions.PytubeError as err:
                print(str(err))

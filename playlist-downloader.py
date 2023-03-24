#!/usr/bin/env python3

import sys
import os
import requests
from subprocess import run
from pytube import Playlist, exceptions
from time import sleep
from alive_progress import alive_bar


playlist = Playlist(sys.argv[1])
videos = [*playlist.videos]
album = playlist.title.removeprefix("Album - ")
artist = videos[0].author.removesuffix(" - Topic")
cover = f"{album}.jpg"
album_length = len(videos)

if not os.path.exists(album):
    os.mkdir(album)
os.chdir(album)

if not os.path.exists(cover):
    with open(cover, "wb") as f:
        f.write(requests.get(videos[0].thumbnail_url).content)
    run(["convert", cover, "-crop", "360x360+140+60", cover])

for i, video in enumerate(playlist.videos, 1):
    for _ in range(3):
        try:
            file = video.streams.get_audio_only()
            title = file.title
            url = file.url
            default_filename = f"{file.default_filename.removesuffix('.mp4')}.mp3"

            if not os.path.exists(default_filename):
                with alive_bar(2, title=f"[{i}/{album_length}] {title}", stats=False, title_length=30, dual_line=True) as bar:
                    bar.text = "Checking age restriction"
                    if video.age_restricted and not video.use_oauth:
                        video.use_oauth = True
                    bar()

                    bar.text = "Downloading video, converting to .mp3 and adding metadata"
                    run([
                        "ffmpeg",
                        "-loglevel", "16",
                        "-i", url,
                        "-i", cover,
                        "-map", "0", "-map", "1",
                        "-metadata", f"title={title}",
                        "-metadata", f"artist={artist}",
                        "-metadata", f"album={album}",
                        "-metadata", f"track={i}/{album_length}",
                        default_filename
                    ])
                    bar()
            break
        except exceptions.PytubeError as err:
            print(str(err))
            sleep(2)

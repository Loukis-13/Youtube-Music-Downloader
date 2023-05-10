#!/usr/bin/env python3

import os
import requests
from subprocess import run
from pytube import Playlist
import argparse


def cover_path(path):
    if os.path.isfile(path):
        return os.path.abspath(path)
    else:
        raise FileNotFoundError()
 
parser = argparse.ArgumentParser(
    prog="YouTube Music Downloader",
    description="Script to download and tag musics from YouTube Music",
    epilog="Thanks to Pytube"
)
parser.add_argument("-a", "--artist", help="name of the artist")
parser.add_argument("-b", "--album", help="name of the album")
parser.add_argument("-c", "--cover", type=cover_path, help="album cover")
parser.add_argument("-t", "--title", action="store_true", help="prompt to change the title of each music")
parser.add_argument("playlist", help="playlist URL")
args = parser.parse_args()

playlist = Playlist(args.playlist)
videos = [*playlist.videos]
album = args.album or playlist.title.removeprefix("Album - ")
artist = args.artist or videos[0].author.removesuffix(" - Topic")
cover = args.cover or f"{album}.jpg"
album_length = len(videos)

if not os.path.exists(album):
    os.mkdir(album)
os.chdir(album)

if not os.path.exists(cover):
    with open(cover, "wb") as f:
        f.write(requests.get(videos[0].thumbnail_url).content)

for i, video in enumerate(videos, 1):
    file = video.streams.get_audio_only()
    title = file.title
    url = file.url
    default_filename = file.default_filename.replace(".mp4", ".mp3")

    if args.title:
        print(f"Default title: {title}")
        title = input("Enter new title (leave empty to not change):") or title

    if not os.path.exists(default_filename):
        print(f"[{i}/{album_length}] {title}")

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

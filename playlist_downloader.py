#!/usr/bin/env python3

import os
import re
import requests
import tempfile
from subprocess import run
from pytube import Playlist, YouTube


def get_album_cover(video: YouTube):
    cover = tempfile.NamedTemporaryFile("w+b")
    cover.write(requests.get(video.thumbnail_url).content)
    return cover


def download_music(url: str, cover: str, metadata: dict):
    filename = re.sub(r'[^\w\s.-]', '', metadata["title"].strip()).replace(' ', '_').strip('._') + ".mp3"

    if not os.path.exists(filename):
        print(f"[{metadata['track']}] {metadata['title']}")

        metaargs = [i for k, v in metadata.items() for i in ("-metadata", f"{k}={v}")]

        run(["ffmpeg", "-loglevel", "16", "-i", url, "-i", cover, "-map", "0", "-map", "1", *metaargs, filename])


def download_playlist(playlist: Playlist):
    videos = [*playlist.videos]
    album = playlist.title.removeprefix("Album - ")
    artist = videos[0].author.removesuffix(" - Topic")
    cover = get_album_cover(videos[0])
    album_length = len(videos)

    if not os.path.exists(album):
        os.mkdir(album)
    os.chdir(album)

    for i, video in enumerate(videos, 1):
        audio = video.streams.get_audio_only()

        metadata = {
            "title": audio.title,
            "artist": artist,
            "album": album,
            "track": f"{i}/{album_length}",
        }

        download_music(audio.url, cover.name, metadata)

    cover.close()


if __name__ == "__main__":
    import argparse

    def cover_path(path):
        if os.path.isfile(path):
            return os.path.abspath(path)
        else:
            raise FileNotFoundError()

    parser = argparse.ArgumentParser(
        prog="YouTube Music Downloader",
        description="Script to download and tag musics from YouTube Music",
        epilog="Thanks to Pytube",
    )
    parser.add_argument("playlist", help="playlist URL")
    # parser.add_argument("-a", "--artist", help="name of the artist")
    # parser.add_argument("-b", "--album", help="name of the album")
    # parser.add_argument("-c", "--cover", type=cover_path, help="album cover")
    # parser.add_argument("-t", "--title", action="store_true", help="prompt to change the title of each music")
    args = parser.parse_args()

    playlist = Playlist(args.playlist)

    download_playlist(playlist)

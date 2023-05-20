# Youtube Music Downloader
These scripts were made to make easier to download musical albums from YouTube.
You can use it as a CLI, an interactive terminal program on your cellphone or as a GUI.

## Requirements
You need to have Pytube and ffmpeg instaled.
```bash
# To install Pytube
pip install pytube

# The ffmpeg instalation depends on your distribution and package manager
# Arch Linux example
pacman -Syu ffmpeg
```

## CLI
To use it as a CLI simply pass the url of the playlist you want to download.
```bash
python playlist_downloader.py 'https://music.youtube.com/playlist?list=OLAK5uy_kO7Am4TX8UkrifQQw3dZbahMXIuJtqGEc'
```

## Use on cellphone
To use the scripts on your smartphone you need to:
* have [Termux](https://termux.dev/) installed
* clone this repository using termux
* install the dependencies
* create a directory names `bin` on your home directory
* link or copy the files from the repository to the `bin` directory (linking is advised, if there is an update you will not need to copy them again)

### Usage
On the video or music that you want to download, go to share, send it to Termux and, on the prompt, choose the option that you want.  

## GUI
If there are some information that you want to change on the musics you can use the GUI to make that easier.
```bash
python gui.py
```
Then input the link, wait for it to load and alter the informations.

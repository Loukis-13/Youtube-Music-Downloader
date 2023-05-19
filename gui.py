import playlist_downloader
import os
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
from pytube import Playlist


PAD = 10
cover = None
album_image = None


def remove_children(parent):
    for child in parent.winfo_children():
        child.destroy()


def change_cover(component, file=None):
    global album_image

    filename = file or askopenfilename()
    if filename:
        img = Image.open(filename)
        album_image = img.filename

        size = tuple(int(250 / img.size[1] * x) for x in img.size)

        image = ImageTk.PhotoImage(img.resize(size))
        component.configure(image=image)
        component.image = image


def show_album(root, url):
    global cover, album_image

    remove_children(root)

    musics, album, artist = [], tk.StringVar(), tk.StringVar()
    try:
        loading = ttk.Progressbar(root, length=200, mode='determinate')
        loading.pack(padx=100, pady=50)
        root.update_idletasks()

        playlist = Playlist(url)
        videos = [*playlist.videos]
        album.set(playlist.title.removeprefix("Album - "))
        artist.set(videos[0].author.removesuffix(" - Topic"))
        album_length = len(videos)
        cover = playlist_downloader.get_album_cover(videos[0])
        album_image = cover.name

        for i, v in enumerate(videos, 1):
            x = v.streams.get_audio_only()
            title = tk.StringVar()
            title.set(x.title)
            musics.append((x, title))

            loading['value'] = i / album_length * 100
            root.update_idletasks()
    except:
        root.destroy()
        return
    else:
        loading.destroy()

    album_cover = tk.Label(root, cursor="hand2")
    album_cover.pack(pady=PAD)
    album_cover.bind("<Button-1>", lambda _: change_cover(album_cover))
    change_cover(album_cover, cover)

    info = tk.Frame(root)
    info.pack(pady=PAD)

    tk.Label(info, text="Artista", font="Helvetica 18 bold").grid(column=0, row=0, padx=PAD)
    tk.Entry(info, textvariable=artist, font="Helvetica 18 bold", justify="center").grid(column=1, row=0, padx=PAD)

    tk.Label(info, text="Álbum", font="Helvetica 18 bold").grid(column=0, row=1, padx=PAD)
    tk.Entry(info, textvariable=album, font="Helvetica 18 bold", justify="center").grid(column=1, row=1, padx=PAD)

    tk.Label(root, text="Músicas", font="Helvetica 18 bold").pack()

    musicas = tk.Frame(root)
    musicas.pack(pady=PAD)

    for i, m in enumerate(musics, 1):
        tk.Label(musicas, font="Helvetica 12", text=i).grid(row=i, column=0)
        tk.Entry(musicas, textvariable=m[1], font="Helvetica 12", width=30, justify="center").grid(row=i, column=1)

    def baixar():
        if not os.path.exists(album.get()):
            os.mkdir(album.get())
        os.chdir(album.get())

        remove_children(root)

        album_length = len(musics)
        for i, (music, title) in enumerate(musics, 1):
            metadata = {
                "title": title.get(),
                "artist": artist.get(),
                "album": album.get(),
                "track": f"{i}/{album_length}",
            }

            tk.Label(root, text=f"[{metadata['track']}] {metadata['title']}", font="Helvetica 18 bold").pack(anchor="w")
            root.update_idletasks()

            playlist_downloader.download_music(music.url, album_image, metadata)

        root.destroy()

    tk.Button(root, command=baixar, text="Baixar").pack(pady=PAD)


root = tk.Tk()
root.title("Youtube Music Downloader")

tk.Label(root, text="Entra com a URL", font="Helvetica 18 bold").pack(pady=PAD)
url = tk.Entry(root, width=80, font="Helvetica 14 bold", justify="center")
url.pack(pady=PAD)
tk.Button(root, text="Ir", command=lambda: show_album(root, url.get())).pack(pady=PAD)

root.mainloop()

if cover:
    cover.close()

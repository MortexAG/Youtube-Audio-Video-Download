import tkinter as tk
from tkinter import CENTER, END, Button, Entry, Label, Frame, messagebox
import yt_dlp
from yt_dlp import YoutubeDL
import sqlite3
import datetime
import texttable
from texttable import Texttable
import history
import os
root = tk.Tk()
root.title("Youtube Downloader")
root.geometry("500x500")

def clear_entry():
    inputlink.delete(0, END)

# Ffmpeg Checks

if os.path.exists("./ffmpeg.exe"):
    pass
else:
    messagebox.showwarning("ffmpeg.exe is Missing", "Please Add ffmpeg.exe To The App's Folder For It To Work Properly")

if os.path.exists("./ffprobe.exe"):
    pass
else:
    messagebox.showwarning("ffprobe.exe is Missing", "Please Add ffprobe.exe To The App's Folder For It To Work Properly")
if os.path.exists("./ffplay.exe"):
    pass
else:
    messagebox.showwarning("ffplay.exe is Missing", "Please Add ffplay.exe To The App's Folder For It To Work Properly")
# Make The Download History

# Create the database if it isn't there
conn = sqlite3.connect('downloads.db')
conn.execute('''CREATE TABLE IF NOT EXISTS downloads
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             name TEXT NOT NULL,
             type_and_time TEXT NOT NULL,
             url TEXT NOT NULL);''')
conn.close()

# Insert The Downloads In A Local Database
def insert_download(name, type, url):
    # Insert a new row into the downloads table with the current date and time
    now = datetime.datetime.now()
    date = now.strftime('%Y-%m-%d')
    time = now.strftime('%H:%M:%S')
    full_time = f"{date}, {time}"
    type_and_time =f"{type}, {full_time}" 
    conn = sqlite3.connect('downloads.db')
    conn.execute(f"INSERT INTO downloads (name, type_and_time, url) VALUES ('{name}', '{type_and_time}','{url}')")
    conn.commit()
    conn.close()
# Retrive The Downloads From The Database And Add Them To A Text File

#def export_to_texttable(filename):
#    # Connect to the database
#    conn = sqlite3.connect('downloads.db')
#    c = conn.cursor()
#
#    # Select all rows from the "downloads" table
#    c.execute("SELECT * FROM downloads")
#    rows = c.fetchall()
#
#    # Create a texttable and add the rows to it
#    table = Texttable()
#    table.set_deco(Texttable.HEADER)
#    table.add_rows([['id','Download Name', 'Type', 'Time']] + rows)
#
#    # Write the texttable to a file
#    with open(filename, 'w') as f:
#        f.write(table.draw())
#
#    # Close the database connection
#    conn.close()
def download_video():
    try:
        thelink = inputlink.get()
        print(thelink)
        ytdl_opts = {
            'outtmpl':'downloads/' + '/%(title)s.%(ext)s',
        }
        with YoutubeDL(ytdl_opts) as ydl: 
            info_dict = ydl.extract_info(thelink, download=False)
            #video_url = info_dict.get("url", None)
            #video_id = info_dict.get("id", None)
            video_title = info_dict.get('title', None)
            print("Title: " + video_title) # <= Here, you got the video title
            ydl.download(thelink)
        insert_download(video_title, 'Video', thelink)
        #export_to_texttable('download history.txt')
        lbl.config(text=f"Downloaded: {video_title}", bg="Green", fg="white")
        clear_entry()
    except Exception as e:
        print(e)
        lbl.config(text="There Was An Error", bg="red", fg="white")
def download_audio():
    try:
        thelink = inputlink.get()
        print(thelink)
        ytdl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'outtmpl':'downloads/' + '/%(title)s.%(ext)s',
        }
        with YoutubeDL(ytdl_opts) as ydl:
            info_dict = ydl.extract_info(thelink, download=False)
            video_title = info_dict.get('title', None)
            print("Title: " + video_title) # <= Here, you got the video title
            ydl.download([thelink])
        insert_download(video_title, 'Audio', thelink)
        #export_to_texttable('download history.txt')
        lbl.config(text=f"Audio Downloaded: {video_title}", bg="Green", fg="white")
        clear_entry()
    except Exception as e:
        print(e)
        lbl.config(text="There Was An Error", bg="red", fg="white")
    

frame=Frame(root, width=300, height=300)
frame.grid(row=0, column=0, sticky="NW")

Label(root, text="Add The Youtube Video Link Here").place(relx=0.5, rely=0.4, anchor=CENTER)

inputlink = Entry(root, width=60)
inputlink.place(relx=0.5, rely=0.5, anchor=CENTER)

Button(root, command=download_video,text="Download Video", activebackground="red", activeforeground="white").place(relx=0.5, rely=0.6, anchor=CENTER)
Button(root, command=download_audio,text="Download Audio", activebackground="red", activeforeground="white").place(relx=0.5, rely=0.7, anchor=CENTER)
Button(root, command= history.main_app, text="Download History",  activebackground="red", activeforeground="white").place(relx=0.5, rely=0.9, anchor=CENTER)
#history.main_app()
lbl = Label(root, text="")
lbl.place(relx=0.5, rely=0.8, anchor=CENTER)
root.mainloop()

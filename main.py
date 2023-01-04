#import tkinter as tk
#from tkinter import Menu, messagebox
#from tkinter import CENTER, END, Button, Entry, Label, Frame
import customtkinter as ctk
from customtkinter import CENTER, END, CTkButton as Button, CTkEntry as Entry, CTkLabel as Label, CTkFrame as Frame, CTkToplevel as Toplevel, CTkCheckBox
import yt_dlp
from yt_dlp import YoutubeDL
import dotenv
from dotenv import load_dotenv
import os

load_dotenv()
root = ctk.CTk()
root.title("Youtube Downloader")
root.geometry("500x500")

confirmation = os.environ['confirm']

ctk.set_default_color_theme("dark-blue")
ctk.set_appearance_mode("dark")
Button(master = root, text="Change Appearance")


def clear_entry():
    inputlink.delete(0, END)

def download_video():
    confirm_it()
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
        lbl.configure(text=f"Downloaded: {video_title}")
        clear_entry()
    except:
        lbl.configure(text="There Was An Error")
def download_audio():
    confirm_it()
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
        lbl.configure(text=f"Audio Downloaded: {video_title}")
        clear_entry()
    except:
        lbl.configure(text="There Was An Error")
    

frame=Frame(root, width=500, height=500)
frame.grid()

Label(root, text="Add The Youtube Video Link Here").place(relx=0.5, rely=0.4, anchor=CENTER)

inputlink = Entry(root, width=400)
inputlink.place(relx=0.5, rely=0.5, anchor=CENTER)

Button(root, command=download_video,text="Download Video").place(relx=0.5, rely=0.6, anchor=CENTER)
Button(root, command=download_audio,text="Download Audio").place(relx=0.5, rely=0.7, anchor=CENTER)

#menu bar

#menubar = Menu(root)
#root.config(menu = menubar)

##### Config Menu

#config_menu = Menu(menubar, tearoff=0)
#config_menu.add_command(label="Change Appearance", command = hola)
#menubar.add_cascade(label = "Config", menu= config_menu)


def confirm_it():
    if confirmation != "True":
        global warning_menu
        warning_menu = Toplevel(root)
        warning_menu.geometry("400x100")
        warning_menu.title("Check ffmpeg Files")
        Label(warning_menu, text="Please Check ffmpeg fies are in the same directory as the program\n or you have them installed on your device").pack()
        Button(master=warning_menu,text="Confirm", command=confirm_btn).pack()

def confirm_btn():
    with open(".env", "w") as configs:
        configs.write("confirm = True")
    warning_menu.destroy()
#def change_mode():
#    global mode
#    mode = "light"
# Warning Menu
confirm_it()
#Button(master=root,text="mode", command=change_mode).place(relx=0.5, rely=0.9, anchor=CENTER)
lbl = Label(root, text="")
lbl.place(relx=0.5, rely=0.8, anchor=CENTER)
root.mainloop()

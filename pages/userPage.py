import tkinter as tk
from tkinter import Scrollbar, ttk
import ttkbootstrap as tkb
from ttkbootstrap.constants import *
from ttkbootstrap.style import Bootstyle
from PIL import Image, ImageTk
from urllib.request import urlopen
import io
import sqlite3

class userPage(tk.Frame):
    def __init__(self, master, app, user):
        super().__init__(master)
        self.master = master
        self.app = app

        self.userPage = tkb.Frame(self)
        self.userPage.pack(fill=BOTH, expand=True)
        
        self.userPage.grid_columnconfigure(0, weight=1)

        ## Check if user was passed through
        if user is not None:
            if self.getUser(user) != "error":
               self.user = self.getUser(user)

        self.createImageFrame()
        self.createUserFrame()




    def createUserFrame(self):
        self.userDetails = tk.Frame(self.userPage,   highlightbackground="#eee", highlightthickness=1)
        self.userInfo = tkb.Frame(self.userDetails)
        self.userName = tkb.Label(self.userInfo, text="USERNAME", font=('Helvetica', 18, 'bold'))
        self.userName.grid(row=0, column=0)
        self.userInfo.grid(row=0, column=0)
        self.userDetails.grid(row=0, column=1, ipadx=100, sticky="NSEW")

    def createImageFrame(self):
        self.imageFrame = tk.Frame(self.userPage,   highlightbackground="#eee", highlightthickness=1)
        response = urlopen(self.user[8])
        data = response.read()
        image = Image.open(io.BytesIO(data))
        image = image.resize((120, 120))
        image = ImageTk.PhotoImage(image=image)
        image_label = tkb.Label(self.imageFrame, image=image)
        image_label.image = image
        image_label.grid(row=0, column=0, sticky=tk.EW, padx=3, pady=3)
        self.imageFrame.grid(row=0, column=0, sticky="NS", ipadx=20)





    def getUser(self, id):
        self.master.cursor.execute(f"SELECT * FROM Users WHERE id={id}")
        user = self.master.cursor.fetchone()
        if user is not None:
            return user
        else:
            return "error"


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
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.content = tkb.Frame(self.app)
        self.content.place(relx=.5, rely=0.55, anchor="c")

        self.cartLabel = tkb.Label(self.content, text="Welcome to your User Profile")
        self.cartLabel.pack()


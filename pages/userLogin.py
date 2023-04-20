import tkinter as tk
from tkinter import Scrollbar, ttk
import ttkbootstrap as tkb
from ttkbootstrap.constants import *
from ttkbootstrap.style import Bootstyle

class userLogin(tk.Frame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app

        self.loginPage = tkb.Frame(self)

        self.exampleLabel = tkb.Label(self.loginPage, text="Welcome to login")
        self.exampleLabel.pack()

        self.loginPage.pack()
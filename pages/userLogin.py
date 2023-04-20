import tkinter as tk
from tkinter import Scrollbar, ttk
import ttkbootstrap as tkb
from ttkbootstrap.constants import *
from ttkbootstrap.style import Bootstyle
from PIL import Image, ImageTk
from urllib.request import urlopen
import io
import sqlite3
 

class userLogin(tk.Frame):
	# self is own frame, master main file, app is the window
	def __init__(self, master, app):
		super().__init__(master)


		self.app = app
		self.loginPage = tkb.Frame(self)

		self.exampleLabel.pack() 



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
		self.app = app

		self.userPage = tkb.Frame(self)
		self.userPage.pack(fill=BOTH, expand=True)

		self.userPage.grid_columnconfigure()

		# Check if user was passed through
		if user is not None:
			if self.getUser(user) != "error":
				self.user = self.getUser(user)

		self.createImageFrame()
		self.createUserFrame()

	def createUserFrame(self):
		self.userDetails = tkb.Frame(self.userPage, width=100)
		
		self.userInfo = tkb.Frame(self.userDetails)
		self.userName = tkb.Label(self.userInfo, text=self.user[3], font=("Helvetica", 18, "bold"))

		self.username.grid(row=0, column=0)
		self.userInfo.grid(row=0, column=0)


		self.userDetails.grid(row=0, column=1, pady=5, ipadx=100, sticky="NW")


	
	def createImageFrame(self):
		# Image container, then read the image from the user 
		self.imageFrame = tkb.Frame(self.userPage, width=60, highlightbackground="#eee", borderwidth=1)
		response = urlopen(self.user[8])
		data = response.read()
		image = Image.open(io.BytesIO(data))
		image = image.resize((120, 120))
		image = ImageTk.PhotoImage(image=image)
		image_label = tkb.Label(self.imageFrame, image=image)
		image_label.image = image
		image_label.grid(row=0, column=0, sticky=tk.EW, padx=3, pady=3)
		self.imageFrame.grid(row=0, column=0, pady=5, ipadx=20, sticky="NE")


	def getUser(self, id):
		self.cursor.execute(f"SELECT * FROM Users WHERE id={id}")
		user = self.cursor.fetchone()
		if user is not None:
			return user
		else:
			return "Error"
		
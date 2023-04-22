import tkinter as tk
from tkinter import Scrollbar, ttk
import ttkbootstrap as tkb
from ttkbootstrap.constants import *
from ttkbootstrap.style import Bootstyle
from PIL import Image, ImageTk
import sqlalchemy as sa
from urllib.request import urlopen
import io
import sqlite3
import hashlib
import sys
import os

# Adds the project directory to a "sys.path" list; think of it as now being in base directory and systematically 
# going down the paths to get the import;
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from classes.User import User
import classes.utilities as Utilities

# Login class for the login page
class userLogin(tk.Frame):
	# self is own frame, master main file, app is the window
	def __init__(self, master, app):
		super().__init__(master)
		self.app = app

		# Create the frame that contains all of the widgets and things on page
		self.loginPage = tkb.Frame(self)
		self.loginPage.pack(expand=True)

		# Create the login message section to alert the user about events in the login page; mainly errors
		self.loginMessageSection = tkb.Frame(self.loginPage)
		self.loginMessageLabel = tkb.Label(self.loginMessageSection, text="")
		self.loginMessageSection.pack(pady=10)
		self.loginMessageLabel.grid(row=0, column=0)

		# Create the login section where you input the information
		self.inputLoginSection = tkb.LabelFrame(self.loginPage, text="Enter credentials to log in")
		self.inputLoginSection.pack(fill=BOTH, expand=True, ipadx=20, ipady=10)
		# Create button section for the login page
		self.loginBtnSection = tkb.Frame(self.inputLoginSection)

		# Create a confirm log in button and a button that takes the user to the account registration/creation page				
		openCreateAccountBtn = tkb.Button(self.loginBtnSection, text="Don't have an account?", command=lambda: self.master.openPage("userRegister")) 
		confirmLoginBtn = tkb.Button(self.loginBtnSection, text="Confirm", command=self.loginUserAccount)
		
		self.fieldNamesLogin = ["Email", "Password"] # List of fields names needed for logging
		self.entryLoginList = [] # List of entry widgets for getting login input, we will then access these widgets later in the loginUserAccount function

		# Create label and entry widgets for each field, and position them; store the entry widgets for later use; then position the button section at the bottom of the grid
		for x in range(len(self.fieldNamesLogin)):
			fieldLabelLogin = tkb.Label(self.inputLoginSection, text=f"{self.fieldNamesLogin[x]}:")
			fieldEntryLogin = tkb.Entry(self.inputLoginSection)
			fieldLabelLogin.grid(row=x, column=0, padx=5, pady=10, ipadx=20)
			fieldEntryLogin.grid(row=x, column=1, padx=5, pady=10, ipadx=20)
			self.entryLoginList.append(fieldEntryLogin)
		
		# Position the button section for the login, and position the buttons themselvse
		self.loginBtnSection.grid(row=len(self.fieldNamesLogin), column=0, columnspan=2, sticky=tk.S)
		openCreateAccountBtn.grid(row=0, column=0, padx=10, pady=10)
		confirmLoginBtn.grid(row=0, column=1, padx=10, pady=10)

	## Checks the email and password that the user entered to log them in, if their information exists in the database
	## We log them in and update id of the current user that's logged in
	def loginUserAccount(self):
		# input validation to make sure they aren't entering blank or whitespace only
		self.entryLoginList = Utilities.stripEntryWidgets(self.entryLoginList)
		if Utilities.isEmptyEntryWidgets(self.entryLoginList):
			self.loginMessageLabel.config(text="Account Login Error: Some fields were left blank")
			return
		
		# Get password from the corresponding entry widget
		inputPassword = self.entryLoginList[1].get()

		with self.master.conn:
			# Get entries that match email and password hash
			self.master.cursor.execute("SELECT * from Users WHERE email=:email AND password_hash=:password_hash", 
			{
				"email": self.entryLoginList[0].get(), "password_hash": hashlib.md5(inputPassword.encode("utf-8")).hexdigest()
			})
			data = self.master.cursor.fetchone()

			# If it's none, there are no accounts from the Users table that match the email or password
			if data is None:
				self.loginMessageLabel.config(text="Username or Password is incorrect")
				return
			
			# If it passes then, the account login was successful, update the current logged in user so whole site can keep track
			# of who is logged in
			self.master.loggedinUser = data[0]
			
		# Change userButton in navbar, now that we've logged in it should say "User" or "My Account" rather than just "login",
		self.master.userButton.configure(text="User", command=lambda: self.master.openPage("userPage", self.master.loggedinUser))
		# Take user to the userPage now that they're logged in, passed the user ID of the current user that's logged in
		self.master.openPage("userPage", self.master.loggedinUser)
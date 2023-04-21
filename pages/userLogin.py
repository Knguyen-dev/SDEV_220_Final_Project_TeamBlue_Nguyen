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

class userLogin(tk.Frame):
	# self is own frame, master main file, app is the window
	def __init__(self, master, app):
		super().__init__(master)
		self.app = app

		# Create the frame that contains all of the widgets and things on page
		self.loginPage = tkb.Frame(self)
		self.loginPage.pack(expand=True)

		# Create the login message section to alert the user about events in the login page
		self.loginMessageSection = tkb.Frame(self.loginPage)
		self.loginMessageSection.pack(pady=10)
		self.loginMessageLabel = tkb.Label(self.loginMessageSection, text="")
		self.loginMessageLabel.grid(row=0, column=0)

		# Create the login section where you input the information
		self.inputLoginSection = tkb.LabelFrame(self.loginPage, text="Enter credentials to log in")
		self.inputLoginSection.pack(fill=BOTH, expand=True, ipadx=20, ipady=10)

		self.loginBtnSection = tkb.Frame(self.inputLoginSection)

		self.fieldNamesLogin = ["Email", "Password"] # List of fields names needed for logging
		self.entryLoginList = [] # List of entry widgets for getting login input, we will then access these widgets later in the loginUserAccount function

		# Create label and entry widgets for each field, and position them; store the entry widgets for later use
		for x in range(len(self.fieldNamesLogin)):
			fieldLabelLogin = tkb.Label(self.inputLoginSection, text=f"{self.fieldNamesLogin[x]}:")
			fieldEntryLogin = tkb.Entry(self.inputLoginSection)
			fieldLabelLogin.grid(row=x, column=0, padx=5, pady=10, ipadx=20)
			fieldEntryLogin.grid(row=x, column=1, padx=5, pady=10, ipadx=20)
			self.entryLoginList.append(fieldEntryLogin)
		
		self.loginBtnSection.grid(row=len(self.fieldNamesLogin), column=0, columnspan=2, sticky=tk.S)

		# Create a confirm log in button and a button that takes the user to the account registration/creation page		
		openCreateAccountBtn = tkb.Button(self.loginBtnSection, text="Don't have an account?", command=lambda: self.master.openPage("userRegister")) 
		confirmLoginBtn = tkb.Button(self.loginBtnSection, text="Confirm", command=self.loginUserAccount)
		openCreateAccountBtn.grid(row=len(self.fieldNamesLogin), column=0, padx=10, pady=10)
		confirmLoginBtn.grid(row=len(self.fieldNamesLogin), column=1, padx=10, pady=10)

	## Checks the email and password that hte user entered to log them in, if their information exists in the database
	## We log them in and update id of the current user that's logged in
	def loginUserAccount(self):
		# input validation to check if any of the inputs are white space 
		for entry in self.entryLoginList:
			if entry.get().strip() == "":
				self.loginMessageLabel.config(text="Account Login Error: Some fields were left blank")
				return
		
		# Get the password input from the corresponding entry widget
		inputPassword = self.entryLoginList[1].get()

		engine = sa.create_engine("sqlite:///assets/PyProject.db")
		with engine.connect() as conn:
			result = conn.execute(sa.text("SELECT * from Users WHERE email=:email AND password_hash=:password_hash"), {"email": self.entryLoginList[0].get(), "password_hash": hashlib.md5(inputPassword.encode("utf-8")).hexdigest()})
			data = result.fetchone() 

			# If it's none, there are no accounts from the Users table that match the email or password
			if data is None:
				self.loginMessageLabel.config(text="Username or Password is incorrect")
				return
			
			# If it passes then, the account login was successful, update the current logged in user so whole site can keep track
			# of who is logged in
			self.master.loggedinUser = data[0]
			
			# Create currentUser instance and update it to represent a class instance of the logged in user for possible usage in the future
			currentUser = User(username=data[1], firstName=data[2], lastName=data[3], shippingAddress=data[6], emailAddress=data[4])
			currentUser.setUserBalance(data[5])
			currentUser.setUserPoints(data[7])

			# Ok so when they login, we actually want to take them to the actual "User account page"
			self.master.openPage("userPage", self.master.loggedinUser)

			


			# password for JeeseJames is 123a

				


		
			



			


		# print(hashlib.md5('password'))





			



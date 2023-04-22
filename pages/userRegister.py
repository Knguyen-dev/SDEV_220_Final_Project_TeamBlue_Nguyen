import tkinter as tk
from tkinter import Scrollbar, ttk
import ttkbootstrap as tkb
from ttkbootstrap.constants import *
from ttkbootstrap.style import Bootstyle
from PIL import Image, ImageTk
from urllib.request import urlopen
import io
import sqlite3
import hashlib

# For making importing easier; essentially think of it as we are in the base project directory now; then we go into the "classes" folder and get our module/python file, then import our class
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from classes.User import User
import classes.utilities as Utilities


class userRegister(tk.Frame):
	# self is own frame, master main file, app is the window
	def __init__(self, master, app):
		super().__init__(master)
		self.app = app

		# Create the frame that will contain all of the widgets and things on the page
		self.registrationPage = tkb.Frame(self)
		self.registrationPage.pack(expand=True)

		# Create section that shows errors and create label that will show errors when creating an account
		self.creationMessageSection = tkb.Frame(self.registrationPage)
		self.creationMessageSection.pack(pady=20)
		self.creationMessageLabel = tkb.Label(self.creationMessageSection, text="")
		self.creationMessageLabel.grid(row=0, column=0) 

		# Create the login section where you input the information
		self.inputCreationSection = tkb.LabelFrame(self.registrationPage, text="Enter credentials to log in")
		self.inputCreationSection.pack(fill=BOTH, expand=True, ipadx=20, ipady=10)

		# Create the button section and put it inside the input section
		self.createBtnSection = tkb.Frame(self.inputCreationSection)

		self.fieldNamesCreate = ["Username", "First Name", "Last Name", "Shipping Address", "Email", "Password", "Retype Password"] # List of fields names needed for creating an account
		self.entryCreateList = [] # List of entry widgets for getting login input, we will then access these widgets later in the loginUserAccount function

		# Create label and entry widgets for each field, and position them; store the entry widgets for later use
		for x in range(len(self.fieldNamesCreate)):
			fieldLabelCreate = tkb.Label(self.inputCreationSection, text=f"{self.fieldNamesCreate[x]}:")
			fieldEntryCreate = tkb.Entry(self.inputCreationSection)
			fieldLabelCreate.grid(row=x, column=0, padx=5, pady=5)
			fieldEntryCreate.grid(row=x, column=1, padx=5, pady=5)
			self.entryCreateList.append(fieldEntryCreate)

		# Have the creationBtnSection at the end of the grid after the fields
		self.createBtnSection.grid(row=len(self.fieldNamesCreate), column=0, columnspan=2, sticky=tk.S, padx=10)

		# Create buttons that open the login page from the registration page and confirm account creation button. 
		openLoginPageBtn = tkb.Button(self.createBtnSection, text="Already have an account?", command=lambda: self.master.openPage("userLogin"))
		confirmCreationBtn = tkb.Button(self.createBtnSection, text="Confirm", command=self.createUserAccount)
		openLoginPageBtn.grid(row=len(self.fieldNamesCreate), column=0, padx=10, pady=10)
		confirmCreationBtn.grid(row=len(self.fieldNamesCreate), column=1, padx=10, pady=10)

	## Function for creating a user account and adding it to the database
	def createUserAccount(self):
		# input validation to make sure they aren't entering blank or whitespace only
		self.entryCreateList = Utilities.stripEntryWidgets(self.entryCreateList)
		if Utilities.isEmptyEntryWidgets(self.entryCreateList):
			self.creationMessageLabel.config(text="Account Creation Error: Some fields were left blank")
			return
			
		# Get password from the corresponding entry widget
		inputPassword = self.entryCreateList[5].get()
		# Check if fields "Password" and "Retype Password" are the same, if they aren't then give them an error message to tell them they did something wrong
		if (inputPassword != self.entryCreateList[6].get()):
			self.creationMessageLabel.config(text="Account Creation Error: Passwords do not match")
			return

		# Create user instance with the input from the input entries
		inputUser = User(username=self.entryCreateList[0].get(), firstName=self.entryCreateList[1].get(), lastName=self.entryCreateList[2].get(), shippingAddress=self.entryCreateList[3].get(), emailAddress=self.entryCreateList[4].get())
		
		with self.master.conn:
			self.master.cursor.execute("SELECT username FROM Users WHERE username=:username", {"username": inputUser.getUsername()})
			data = self.master.cursor.fetchone()

			# If there's an username entry in the database with the same username as the one that was inputted, then we get an error when creating the account since usernames are supposed to be unique
			if data is not None:
				self.creationMessageLabel.config(text=f"Account Creation Error: '{inputUser.getUsername()}' is already taken")
				return
			
			# Account creation is successful, add it to the database and save database
			self.master.cursor.execute("INSERT INTO Users (username, fname, lname, email, balance, address, points, password_hash, avatar) VALUES (:username, :fname, :lname, :email, :balance, :address, :points, :password_hash, :avatar)",
			{
			"username": inputUser.getUsername(),
			"fname": inputUser.getFirstName(),
			"lname": inputUser.getLastName(),
			"email": inputUser.getEmailAddress(),
			"balance": inputUser.getBalance(),
			"address": inputUser.getShippingAddress(),
			"points": inputUser.getPoints(),
			# Hash the password with an algorithm and store it as a one of the values for the database entry
			"password_hash": hashlib.md5(inputPassword.encode("utf-8")).hexdigest(),
			# Set their avatar or profile picture to a default image in the database; so all accounts start off with default image
			"avatar": "https://st3.depositphotos.com/1767687/16607/v/600/depositphotos_166074422-stock-illustration-default-avatar-profile-icon-grey.jpg"
			})

		# Now that they've successfully created the account we take them to the login page so that they can login with their new information
		self.master.openPage("userLogin")

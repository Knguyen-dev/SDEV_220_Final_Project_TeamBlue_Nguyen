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
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from classes.User import User
import classes.utilities as Utilities

class userChangePassword(tk.Frame): 
	def __init__(self, master, app):
		super().__init__(master)
		self.app = app
		self.master = master

		# Create the change password page
		self.passwordPage = tkb.Frame(self)
		self.passwordPage.pack(expand=True)

		# Create message section and label for showing error and other messages to the suer
		self.passwordMessageSection = tkb.Frame(self.passwordPage)
		self.passwordMessageLabel = tkb.Label(self.passwordMessageSection, text="")
		self.passwordMessageSection.pack()
		self.passwordMessageLabel.grid(row=0, column=0)

		# Create section for inputting credentials for changing your password
		self.inputPasswordSection = tkb.LabelFrame(self.passwordPage, text="Enter Password Info")
		self.inputPasswordSection.pack(ipadx=20, padx=20, pady=10)

		# Create field names, these will be the input fields they fill out to ocnfirm a password change
		self.fieldNamesPassword = ["Current Password", "New Password", "Retype Password"]
		# List will include our entry widgets that correspond to our fields; a parallel list to fieldNamesPassword
		self.entryPasswordList = []
		
		# Create our label and entry widgets, then position them; also store our entry widgets
		for x in range(len(self.fieldNamesPassword)):
			fieldLabelPassword = tkb.Label(self.inputPasswordSection, text=f"{self.fieldNamesPassword[x]}:")
			fieldEntryPassword = tkb.Entry(self.inputPasswordSection)
			fieldLabelPassword.grid(row=x, column=0, padx=5, pady=10)
			fieldEntryPassword.grid(row=x, column=1, padx=5, pady=10)
			self.entryPasswordList.append(fieldEntryPassword)

		# Create button section for the change password page; 
		# Nest this section in the inputPasswordSection and put it under the labels and widgets
		self.passwordBtnSection = tkb.Frame(self.inputPasswordSection)
		self.passwordBtnSection.grid(row=len(self.fieldNamesPassword), column=0, columnspan=2, pady=10)

		# Create button for confirming your password change
		self.changePasswordBtn = tkb.Button(self.passwordBtnSection, text="Confirm Password Change", command=self.changeUserPassword)
		self.changePasswordBtn.grid(row=0, column=0) 

	## Function that confirms password change for current user account as long as it passes checks
	def changeUserPassword(self):
		# Strip trailing and leading whitespace from entry widgets
		self.entryPasswordList = Utilities.stripEntryWidgets(self.entryPasswordList)
		if Utilities.isEmptyEntryWidgets(self.entryPasswordList):
			self.passwordMessageLabel.config(text="Error: Some pages were left blank")
			return 
		# Check if the new password and retyped password are amtching
		if (self.entryPasswordList[1].get() != self.entryPasswordList[2].get()):
			self.passwordMessageLabel.config(text="New password and retyped password don't match")
			return
		
		# Get their inputted current password and input for the new password 
		inputCurrentPassword = self.entryPasswordList[0].get()
		inputNewPassword = self.entryPasswordList[1].get()

		# Password has passed all checks, so now update the user's password in the User table
		with self.master.conn:
			
			# Check if the input for current password matches their current password
			self.master.cursor.execute(f"SELECT password_hash FROM Users WHERE id=:id", {"id": self.master.loggedinUser})
			
			# Query the password hash for the user from the database
			dbPasswordHash = self.master.cursor.fetchone()[0]

			# Check if current password they put in matches the one in the database by comparing their md5 hashes
			if (hashlib.md5(inputCurrentPassword.encode("utf-8")).hexdigest() != dbPasswordHash):
				self.passwordMessageLabel.config(text="Your inputted password is incorrect")
				return

			# All tests were passed so we update their password in the database
			self.master.cursor.execute(f'''UPDATE Users SET password_hash=:password_hash WHERE id=:id''', 
			{
				"password_hash": hashlib.md5(inputNewPassword.encode("utf-8")).hexdigest(),
				"id": self.master.loggedinUser
			})
		# Log out the user after
		self.master.logOutUser()

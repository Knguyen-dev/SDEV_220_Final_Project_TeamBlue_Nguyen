import tkinter as tk
from tkinter import ttk
import hashlib
import classes.utilities as Utilities

# Page used for deleting the account of the current logged in user
class userDelete(tk.Frame):
	def __init__(self, master, app):
		super().__init__(master)
		self.app =  app
		self.master = master
		
		# Create the page section
		self.deletePage = ttk.Frame(self)
		self.deletePage.pack(expand=True)

		# create message section that will alert the user about events on the delete account page
		self.deleteMessageSection = ttk.Frame(self.deletePage)
		self.deleteMessageLabel = ttk.Label(self.deleteMessageSection, text="")
		self.deleteMessageSection.pack(pady=10)
		self.deleteMessageLabel.grid(row=0, column=0)

		# Create sectikno for inputting information to delete the account of the current logged in user
		self.inputDeleteSection = ttk.LabelFrame(self.deletePage, text="Enter credentials of the currently logged in account")
		self.inputDeleteSection.pack(ipadx=5, ipady=10)

		# Button section for delete page; mainly just going to be the delete button itself for now
		self.deleteBtnSection = ttk.Frame(self.inputDeleteSection)
		self.confirmDeleteBtn = ttk.Button(self.deleteBtnSection, text="Delete Account", command=self.deleteUserAccount)

		# Field names needed to delete your account; using username instead of email because username is unique
		self.fieldNamesDelete = ["Username", "Password", "Retype Password"]
		self.entryDeleteList = []

		# Create labels and entry widgest, position them, and position the deleteBtnSection at teh bottom
		for x in range(len(self.fieldNamesDelete)):
			fieldLabelDelete = ttk.Label(self.inputDeleteSection, text=f"{self.fieldNamesDelete[x]}:")
			fieldEntryDelete = ttk.Entry(self.inputDeleteSection)
			fieldLabelDelete.grid(row=x, column=0, padx=5, pady=10)
			fieldEntryDelete.grid(row=x, column=1, padx=5, pady=10)
			self.entryDeleteList.append(fieldEntryDelete)
		self.deleteBtnSection.grid(row=len(self.fieldNamesDelete), column=0, columnspan=2)
		self.confirmDeleteBtn.grid(row=0,column=0)

	def deleteUserAccount(self):
		# Strip entry widgets and check if some fields were left blank
		self.entryDeleteList = Utilities.stripEntryWidgets(self.entryDeleteList)
		if Utilities.isEmptyEntryWidgets(self.entryDeleteList):
			self.deleteMessageLabel.config(text="Account Deletion Error: Some fields were left blank")
			return
		
		inputPassword = self.entryDeleteList[1].get()
		# Check if password and retyped password match
		if (inputPassword != self.entryDeleteList[2].get()):
			self.deleteMessageLabel.config(text="Password and retyped password don't match")
			return
		
		with self.master.conn:
			# We want to make sure that they are deleting the current account, and not just any account in the database, so include loggedinUser. This is because if they try to enter info from another account, the
			# id is there to make sure to filter to only get the current logged in user account.
			self.master.cursor.execute("SELECT * FROM Users WHERE username=:username AND password_hash=:password_hash AND id=:id", 
			{
				"username": self.entryDeleteList[0].get(),
				"password_hash": hashlib.md5(inputPassword.encode("utf-8")).hexdigest(),
				"id": self.master.loggedinUser
			})
			data = self.master.cursor.fetchone()

			# This would mean the input for username and pasword does not match the current logged in account, so we will pass an error message
			if data is None:
				self.deleteMessageLabel.config(text="Username or Password is incorrect. Make sure you're entering the info of the currently logged in user.")
				return 
			
			# At this point it means that the user has entered the correct information, so we delete their account from the database
			self.master.cursor.execute("DELETE FROM Users WHERE id=:id", 
			{
				"id": self.master.loggedinUser
			})		
		# After correctly deleting the current user, set the logged in user back to None 
		# Set the userButton so that when pressed it sends you to the login page. 
		# After they've deleted their account, take them to the account registration page
		self.master.logOutUser()


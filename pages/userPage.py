import tkinter as tk
from tkinter import Scrollbar, ttk
import ttkbootstrap as tkb
from ttkbootstrap.constants import *
from ttkbootstrap.style import Bootstyle
from PIL import Image, ImageTk
from urllib.request import urlopen
import io
import sqlite3

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from classes.User import User

# Class represents the userPage or my account page. To get to this page the user should go through the login process first, which 
# ensures that an account exists to create this page for.
class userPage(tk.Frame):
	def __init__(self, master, app, userID):
		super().__init__(master)
		self.master = master
		self.app = app
		
		# Create the frame where all of the user information will lay
		self.userPage = tkb.Frame(self)
		self.userPage.pack(fill=BOTH, expand=True)
		self.userPage.grid_columnconfigure(0, weight=1)
		
		# Get row of data (tuple) that corresponds with "userID" from the Users tabele 
		self.userData = self.getUser(userID)
		
		# Create instance of "User" class with that userData, this represents the class instance of the current logged in user
		# Also update the balance and points attributes since their attributes are defaulted to zero when creating a User instanec
		self.currentUser = User(self.userData[1], self.userData[2], self.userData[3], self.userData[6], self.userData[4])
		self.currentUser.setUserBalance(self.userData[5])
		self.currentUser.setUserPoints(self.userData[7])
		# should also update the points and balance

		# Represents the http URL for the image
		self.userAvatarSource = self.userData[9] 

		# Represents names of user attribute from the User class
		self.userAttributeNames = ["Username", "First Name", "Last Name", "Email", "Shipping Address", "Balance", "Points"]

		self.createImageFrame()
		self.createUserFrame()

	def createUserFrame(self):
		# Create section that stores all of the details for the user account; giving room for account manipulation and other feature elements
		self.userDetailsSection = tkb.LabelFrame(self.userPage, borderwidth=2, relief="groove")
		self.userDetailsSection.grid(row=0, column=1, ipadx=100, sticky="NSEW")

		# Create section that only stores user info and create section that contain recent purchases; nest both of those in the userDetailsSection section
		self.userInfoSection = tkb.LabelFrame(self.userDetailsSection, text="User information")
		self.userInfoSection.grid(row=0, column=0)
		self.recentPurchasesSection = tkb.LabelFrame(self.userDetailsSection, text="Recent Purchases", borderwidth=2, relief="groove")
		self.recentPurchasesSection.grid(row=1, column=0)

		# Here's an example purchase to see where the purchase section is
		self.samplePurchase = tkb.Label(self.recentPurchasesSection, text="1. Example Purchase")

		'''
		Here would be a for loop to loop through all of those purchases and grid them on the recent purchase section
		
		'''
		self.samplePurchase.grid(row=0, column=0)


		# Create section that contains buttons relating to manipulating the user's account (account settings), such as logging out, editing account info, etc.
		self.accountSettingsSection = tkb.LabelFrame(self.userDetailsSection, text="Account Settings", borderwidth=2, relief="groove")
		self.accountSettingsSection.grid(row=2, column=0)

		# create buttons for logging out user, and opening the pages where you edit or delete your account 
		self.openEditAccountBtn = tkb.Button(self.accountSettingsSection, text="Edit Account", command=lambda: self.master.openPage("userEdit", self.currentUser))
		self.openManageBalanceBtn = tkb.Button(self.accountSettingsSection, text="Manage Wallet Balance")
		self.logOutBtn = tkb.Button(self.accountSettingsSection, text="Log Out", command=self.logOutUser)
		self.openDeleteAccountBtn = tkb.Button(self.accountSettingsSection, text="Delete Account", command=lambda: self.master.openPage("userDelete"))
		# Position those buttons
		self.openEditAccountBtn.grid(row=0, column=0, padx=5, pady=5)
		self.openManageBalanceBtn.grid(row=1, column=0, padx=5, pady=5)
		self.logOutBtn.grid(row=2, column=0, padx=5, pady=5)
		self.openDeleteAccountBtn.grid(row=3, column=0, padx=5, pady=5)

		# Create labels for all of the user's attributes using the names of those attributes
		for x in range(len(self.userAttributeNames)):
			userAttributeLabel = tkb.Label(self.userInfoSection, text=f"{self.userAttributeNames[x]}: {self.currentUser.getAttributeByName(self.userAttributeNames[x])}")
			userAttributeLabel.grid(row=x, column=0)

	# Create image section
	def createImageFrame(self):
		self.imageFrame = tkb.Frame(self.userPage)
		response = urlopen(self.userAvatarSource)
		data = response.read()
		image = Image.open(io.BytesIO(data))
		image = image.resize((120, 120))
		image = ImageTk.PhotoImage(image=image)
		image_label = tkb.Label(self.imageFrame, image=image)
		image_label.image = image
		image_label.grid(row=0, column=0, sticky=tk.EW, padx=3, pady=3)
		self.imageFrame.grid(row=0, column=0, sticky="NS", ipadx=20)

	# Get the user information; login process guarantees that an existing and valid userID exists, so we can be sure that this query always brings the right user data
	def getUser(self, id):
		self.master.cursor.execute(f"SELECT * FROM Users WHERE id={id}")
		user = self.master.cursor.fetchone()
		return user
	
	## Logs out the user by clearing the loggedinUser variable, and taking user to the login page
	def logOutUser(self):
		self.master.loggedinUser = None
		# Change userButton so that it redirects to the login page 
		self.master.userButton.configure(text="Login", command=lambda: self.master.openPage("userLogin"))
		self.master.openPage("userLogin")
		return
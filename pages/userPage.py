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
		self.currentUser = User(self.userData[1], self.userData[2], self.userData[2], self.userData[6], self.userData[4])
		self.currentUser.setUserBalance(self.userData[5])
		self.currentUser.setUserPoints(self.userData[7])
		# should also update the points and balance

		# Represents the http URL for the image
		self.userAvatarSource = self.userData[9] 


		# BOOK MARK: Create current user class instance, maybe try hand at some styling, but 
		# getting the class instance and being able to have all of the class information is key 
		# Should commit when login and registration is done and userPage has been linked

		# attribute names for the user class instance  

		# BOOK MARK: Something wrong with attribute mapper
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

		# Create section that contains buttons relating to manipulating the user's account (account settings), such as logging out, editing account info, etc.
		self.accountSettingsSection = tkb.LabelFrame(self.userDetailsSection, text="Account Settings", borderwidth=2, relief="groove")
		self.accountSettingsSection.grid(row=2, column=0)

		# create buttons for logging out user, and opening the pages where you edit or delete your account 
		self.openEditAccountBtn = tkb.Button(self.accountSettingsSection, text="Edit Account")
		self.openManageBalanceBtn = tkb.Button(self.accountSettingsSection, text="Manage Wallet Balance")
		self.logOutBtn = tkb.Button(self.accountSettingsSection, text="Log Out")
		self.openDeleteAccountBtn = tkb.Button(self.accountSettingsSection, text="Delete Account")

		# Position those buttons
		self.openEditAccountBtn.grid(row=0, column=0, padx=5, pady=5)
		self.openManageBalanceBtn.grid(row=1, column=0, padx=5, pady=5)
		self.logOutBtn.grid(row=2, column=0, padx=5, pady=5)
		self.openDeleteAccountBtn.grid(row=3, column=0, padx=5, pady=5)




		# BOOK MARK: AT LEAST FINISH TRYING TO CREATE SECTIONS FOR THE FUTURE BUTTONS. THEN COMMIT AND DO ACCOUNT EDITING PAGE, LOGOUT FEATURE,
		# AND DELETE ACCOUNT PAGE

		# Create labels for all of the user's attributes using the names of those attributes
		for x in range(len(self.userAttributeNames)):
			userAttributeLabel = tkb.Label(self.userInfoSection, text=f"{self.userAttributeNames[x]}: {self.currentUser.getAttributeByName(self.userAttributeNames[x])}")
			userAttributeLabel.grid(row=x, column=0)


		# self.userName = tkb.Label(self.userInfoSection, text="USERNAME", font=('Helvetica', 18, 'bold'))
		# self.userName.grid(row=0, column=0)

	def createImageFrame(self):
		self.imageFrame = tk.Frame(self.userPage,   highlightbackground="#eee", highlightthickness=1)
		response = urlopen(self.userAvatarSource)
		data = response.read()
		image = Image.open(io.BytesIO(data))
		image = image.resize((120, 120))
		image = ImageTk.PhotoImage(image=image)
		image_label = tkb.Label(self.imageFrame, image=image)
		image_label.image = image
		image_label.grid(row=0, column=0, sticky=tk.EW, padx=3, pady=3)
		self.imageFrame.grid(row=0, column=0, sticky="NS", ipadx=20)

	def getUser(self, id):
		self.master.cursor.execute(f"SELECT * FROM Users WHERE id={id}")
		user = self.master.cursor.fetchone()
		if user is not None:
			return user
		else:
			return "error"
	
	## Logs out the user by clearing the loggedinUser variable, and taking user to the login page
	def logOutUser(self):
		# it's going to take the user to the login page
		# it's going to make the loggedinUser value None

		self.master.loggedinUser = None
		self.master.openPage("userLogin")
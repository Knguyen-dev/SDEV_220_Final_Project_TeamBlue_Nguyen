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

		# Get row of data (tuple) that corresponds with "userID" from the Users tabele 
		self.userData = self.getUser(userID)
		
		# Create instance of "User" class with that userData, this represents the class instance of the current logged in user
		# Also update the balance and points attributes since their attributes are defaulted to zero when creating a User instanec
		self.currentUser = User(self.userData[1], self.userData[2], self.userData[3], self.userData[6], self.userData[4])
		self.currentUser.setUserBalance(self.userData[5])
		self.currentUser.setUserPoints(self.userData[7])

		# Represents the http URL for the image
		self.userAvatarSource = self.userData[9] 

		# Represents names of user attribute from the User class
		self.userAttributeNames = ["Username", "First Name", "Last Name", "Email", "Shipping Address", "Balance", "Points"]

		# Call functions that create image and user frames
		self.createImageFrame()
		self.createUserFrame()
		self.createProfileBtnsSection()


	# Create an edit profile button that takes them to the edit account page and position it
	def createProfileBtnsSection(self):
		# Create section for containing buttons to manage your account
		self.profileBtnsSection = tkb.Frame(self.userPage)
		self.profileBtnsSection.grid(row=1, column=0)
		# Create and position buttons for the profileBtnsSection
		self.openEditAccountBtn = tkb.Button(self.profileBtnsSection, text="Edit Account", command=lambda: self.master.openPage("userEdit", self.currentUser))
		self.openManageBalanceBtn = tkb.Button(self.profileBtnsSection, text="Manage Wallet", command=lambda: self.master.openPage("userManageBalance", self.currentUser))
		self.logOutBtn = tkb.Button(self.profileBtnsSection, text="Log out", command=self.master.logOutUser)
		self.openDeleteAccountBtn = tkb.Button(self.profileBtnsSection, text="Delete Account", command=lambda: self.master.openPage("userDelete"))
		self.openEditAccountBtn.grid(row=0, column=0, padx=5, pady=5)
		self.openManageBalanceBtn.grid(row=1, column=0, padx=5, pady=5)
		self.logOutBtn.grid(row=2, column=0, padx=5, pady=5)
		self.openDeleteAccountBtn.grid(row=3, column=0, padx=5, pady=5)


	def createRecentPurchasesSection():
		pass

	## Create frame or section to show user information 
	def createUserFrame(self):
		# Create main section for all user information 
		self.userDetailsSection = tk.Canvas(self.userPage, width=100, bg="red")
		# Create section for show user account or user instance attributes
		self.userInfoSection = tkb.Frame(self.userDetailsSection)

		# Put all labels in userInfoSection
		# Create username label, make it big and visible since for aesthetic purposes
		usernameLabel = tkb.Label(self.userInfoSection, text=f"{self.userAttributeNames[0]}: {self.currentUser.getUsername()}", font=('Helvetica', 32, 'bold'))
		usernameLabel.grid(row=0, column=0, columnspan=3, padx=20, pady=10)

		# Create labels for the other attributes for the user; exclude username from iteration
		# We start at 1 because we want to avoid row index 0 since the username label is already occupying that entire row 
		for x in range(1, len(self.userAttributeNames)):
			userAttributeLabel = tkb.Label(self.userInfoSection, text=f"{self.userAttributeNames[x]}: {self.currentUser.getAttributeByName(self.userAttributeNames[x])}", font=("Helvetica", 18, "bold"))
			userAttributeLabel.grid(row=x, column=0, pady=5)
			
		# Position userDetailsSection on the userPage
		self.userInfoSection.pack(fill=X)
		self.userDetailsSection.grid(row=0, column=1, sticky=tk.N, padx=(150, 200))


	## Create frame or section to show the image or avatar of the user's account
	def createImageFrame(self):
		self.imageFrame = tk.Canvas(self.userPage, highlightbackground="#eee", highlightthickness=1)
		response = urlopen(self.userAvatarSource)
		data = response.read()
		image = Image.open(io.BytesIO(data))
		image = image.resize((350, 350))
		image = ImageTk.PhotoImage(image=image)
		image_label = tkb.Label(self.imageFrame, image=image)
		image_label.image = image
		image_label.grid(row=0, column=0, sticky=tk.EW, padx=3, pady=3)
		self.imageFrame.grid(row=0, column=0, padx=40)
	

	# Get the user information; login process guarantees that an existing and valid userID exists, so we can be sure that this query always brings the right user data
	def getUser(self, id):
		self.master.cursor.execute(f"SELECT * FROM Users WHERE id={id}")
		user = self.master.cursor.fetchone()
		return user
	
	# ## Logs out the user by clearing the loggedinUser variable, and taking user to the login page
	# def logOutUser(self):
	# 	self.master.loggedinUser = None
	# 	# Change userButton so that it redirects to the login page 
	# 	self.master.userButton.configure(text="Login", command=lambda: self.master.openPage("userLogin"))
	# 	self.master.openPage("userLogin")
	# 	return
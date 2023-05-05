import tkinter as tk
from tkinter import ttk
import hashlib
import re
from classes.User import User
import classes.utilities as Utilities


class userRegister(tk.Frame):
	# self is own frame, master main file, app is the window
	def __init__(self, master, app):
		super().__init__(master)
		self.app = app
		self.master = master

		# Create the frame that will contain all of the widgets and things on the page
		self.registrationPage = ttk.Frame(self)
		self.registrationPage.pack(expand=True)

		# Email validation Regex
		self.regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

		# Create section that shows errors and create label that will show errors when creating an account
		self.creationMessageSection = ttk.Frame(self.registrationPage)
		self.creationMessageSection.pack(pady=20)
		self.creationMessageLabel = ttk.Label(self.creationMessageSection, text="", foreground="#cc0000")
		self.creationMessageLabel.grid(row=0, column=0) 

		# Create the login section where you input the information
		self.inputCreationSection = ttk.LabelFrame(self.registrationPage, text="Enter credentials to log in")
		self.inputCreationSection.pack(fill='both', expand=True, ipadx=20, ipady=10)

		# Create the button section and put it inside the input section
		self.createBtnSection = ttk.Frame(self.inputCreationSection)

		self.fieldNamesCreate = ["Username", "First Name", "Last Name", "Shipping Address", "Email"] # List of fields names needed for creating an account
		self.entryCreateList = [] # List of entry widgets for getting login input, we will then access these widgets later in the loginUserAccount function

		# Create label and entry widgets for each field, and position them; store the entry widgets for later use
		for x in range(len(self.fieldNamesCreate)):
			fieldLabelCreate = ttk.Label(self.inputCreationSection, text=f"{self.fieldNamesCreate[x]}:")
			fieldEntryCreate = ttk.Entry(self.inputCreationSection,validate='focusout', validatecommand=(self.register(self.validateForm), '%P'))
			fieldLabelCreate.grid(row=x, column=0, padx=5, pady=5)
			fieldEntryCreate.grid(row=x, column=1, padx=5, pady=5)
			self.entryCreateList.append(fieldEntryCreate)

		passwordLabel = ttk.Label(self.inputCreationSection, text="Password: ")
		passwordEntry = ttk.Entry(self.inputCreationSection, show="*")
		passwordLabel.grid(row=5, column=0, padx=5, pady=5)
		passwordEntry.grid(row=5, column=1, padx=5, pady=5)
		self.entryCreateList.append(passwordEntry)

		password2Label = ttk.Label(self.inputCreationSection, text="Confirm Password:")
		password2Entry = ttk.Entry(self.inputCreationSection, show="*")
		password2Label.grid(row=6, column=0, padx=5, pady=5)
		password2Entry.grid(row=6, column=1, padx=5, pady=5)
		self.entryCreateList.append(password2Entry)


		# Have the creationBtnSection at the end of the grid after the fields
		self.createBtnSection.grid(row=7, column=0, columnspan=2, sticky=tk.S, padx=10)

		# Create buttons that open the login page from the registration page and confirm account creation button. 
		openLoginPageBtn = ttk.Button(self.createBtnSection, text="Already have an account?", command=lambda: self.master.openPage("userLogin"))
		confirmCreationBtn = ttk.Button(self.createBtnSection, text="Confirm", command=self.createUserAccount)
		openLoginPageBtn.grid(row=len(self.fieldNamesCreate), column=0, padx=10, pady=10)
		confirmCreationBtn.grid(row=len(self.fieldNamesCreate), column=1, padx=10, pady=10)


	def validateForm(self, input):
		self.regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
		## If the input is empty return false
		if input == "":
			return False
		## If the input is greater than 50 return false
		elif len(input) > 50:
			return False
		elif input == self.entryCreateList[4].get() and not re.fullmatch(self.regex, input):
			return False
		## Everything else passes the Validation
		else:
			return True
	
	## Function for creating a user account and adding it to the database
	def createUserAccount(self):
		# input validation to make sure they aren't entering blank or whitespace only
		self.entryCreateList = Utilities.stripEntryWidgets(self.entryCreateList)
		if Utilities.isEmptyEntryWidgets(self.entryCreateList):
			self.creationMessageLabel.config(text="Account Creation Error: Some fields were left blank", foreground="#cc0000")
			return
		# Input validation for the email, makes sure it is the correct format
		if not re.fullmatch(self.regex, self.entryCreateList[4].get()):
			self.creationMessageLabel.config(text = "Account Creation Error: Email not valid", foreground="#cc0000")
			self.entryCreateList[4].config(highlightcolor="#cc0000")
			return
		# Get password from the corresponding entry widget
		inputPassword = self.entryCreateList[5].get()
		# Check if fields "Password" and "Retype Password" are the same, if they aren't then give them an error message to tell them they did something wrong
		if (inputPassword != self.entryCreateList[6].get()):
			self.creationMessageLabel.config(text="Account Creation Error: Passwords do not match", foreground="#cc0000")
			return

		# Create user instance with the input from the input entries
		inputUser = User(username=self.entryCreateList[0].get(), firstName=self.entryCreateList[1].get(), lastName=self.entryCreateList[2].get(), shippingAddress=self.entryCreateList[3].get(), emailAddress=self.entryCreateList[4].get())
		
		with self.master.conn:
			self.master.cursor.execute("SELECT username FROM Users WHERE username=:username", {"username": self.entryCreateList[0].get()})
			data = self.master.cursor.fetchone()

			# If there's an username entry in the database with the same username as the one that was inputted, then we get an error when creating the account since usernames are supposed to be unique
			if data is not None:
				self.creationMessageLabel.config(text=f"Account Creation Error: '{self.entryCreateList[0].get()}' is already taken")
				return
			
			# Account creation is successful, add it to the database and save database
			self.master.cursor.execute("INSERT INTO Users (username, fname, lname, email, balance, address, points, password_hash, avatar) VALUES (:username, :fname, :lname, :email, :balance, :address, :points, :password_hash, :avatar)",
			{
			"username": self.entryCreateList[0].get(),
			"fname": self.entryCreateList[1].get(),
			"lname": self.entryCreateList[2].get(),
			"email": self.entryCreateList[4].get(),
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

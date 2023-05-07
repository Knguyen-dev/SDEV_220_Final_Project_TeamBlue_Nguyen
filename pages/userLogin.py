import tkinter as tk
from tkinter import ttk
import hashlib
from classes.User import User
import classes.utilities as Utilities

# Login class for the login page
class userLogin(tk.Frame):
	# self is own frame, master main file, app is the window
	def __init__(self, master, app):
		super().__init__(master)
		self.app = app
		self.master = master

		# Create the frame that contains all of the widgets and things on page
		self.loginPage = ttk.Frame(self)
		self.loginPage.pack(expand=True)

		# Create the login message section to alert the user about events in the login page; mainly errors
		loginMessageSection = ttk.Frame(self.loginPage)
		loginMessageSection.pack(pady=10)
		self.loginMessageLabel = ttk.Label(loginMessageSection, text="")
		self.loginMessageLabel.grid(row=0, column=0)

		# Create the login section where you input the information
		self.inputLoginSection = ttk.LabelFrame(self.loginPage, text="Enter credentials to log in")
		self.inputLoginSection.pack(fill='both', expand=True, ipadx=20, ipady=10)
		# Create button section for the login page
		self.loginBtnSection = ttk.Frame(self.inputLoginSection)

		# Create a confirm log in button and a button that takes the user to the account registration/creation page				
		openCreateAccountBtn = ttk.Button(self.loginBtnSection, text="Don't have an account?", command=lambda: self.master.openPage("userRegister")) 
		confirmLoginBtn = ttk.Button(self.loginBtnSection, text="Confirm", command=self.loginUserAccount)
		
		self.entryLoginList = [] # List of entry widgets for getting login input, we will then access these widgets later in the loginUserAccount function
		
		usernameLabel = ttk.Label(self.inputLoginSection, text="Username:")
		usernameEntry = ttk.Entry(self.inputLoginSection)
		usernameLabel.grid(row=0, column=0, padx=5, pady=10, ipadx=20)
		usernameEntry.grid(row=0, column=1, padx=5, pady=10, ipadx=20)
		self.entryLoginList.append(usernameEntry)

		passwordLabel = ttk.Label(self.inputLoginSection, text="Password:")
		passwordEntry = ttk.Entry(self.inputLoginSection, show="*")
		passwordLabel.grid(row=1, column=0, padx=5, pady=10, ipadx=20)
		passwordEntry.grid(row=1, column=1, padx=5, pady=10, ipadx=20)
		self.entryLoginList.append(passwordEntry)
		
		# Position the button section for the login, and position the buttons themselvse
		self.loginBtnSection.grid(row=2, column=0, columnspan=2, sticky=tk.S)
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
			# Get entries that match username and password hash
			# We are using username to log in because that's unique to every account
			self.master.cursor.execute("SELECT * from Users WHERE username=:username AND password_hash=:password_hash", 
			{
				"username": self.entryLoginList[0].get(), "password_hash": hashlib.md5(inputPassword.encode("utf-8")).hexdigest()
			})
			data = self.master.cursor.fetchone()

			# If it's none, there are no accounts from the Users table that match the email or password
			if data is None:
				self.loginMessageLabel.config(text="Username or Password is incorrect")
				return
			
			# If it passes then, the account login was successful, update the current logged in user so whole site can keep track
			# of who is logged in
			self.master.loggedinUser =  User(data[0], data[1], data[2], data[3], data[6], data[9], data[4], data[7], data[5])
			
		# Change userButton in navbar, now that we've logged in it should say "User" or "My Account" rather than just "login",
		self.master.userButton.configure(text="User", command=lambda: self.master.openPage("userPage"))
		# Change the shopping cart button so that it actually takes you to a shopping cart
		self.master.cartButton.configure(command=lambda: self.master.openPage("cartPage"))
		# Take user to the userPage now that they're logged in, passed the user ID of the current user that's logged in
		self.master.openPage("userPage")
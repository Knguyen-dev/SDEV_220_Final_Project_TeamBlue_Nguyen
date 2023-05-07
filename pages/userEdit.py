import tkinter as tk
from tkinter import ttk
from classes.User import User
import classes.utilities as Utilities

# Class or page for editing the current user's account; for changing account information such as name, email, etc.
# NOTE: Page will link to pages for changing the user's password and managing the user's wallet
class userEdit(tk.Frame): 
	def __init__(self, master, app):
		super().__init__(master)
		self.app = app
		self.master = master

		# Create the frame that contains all the widgets and elements on the editPage
		self.editPage = ttk.Frame(self)
		self.editPage.pack(expand=True)
		
		# Create message section that will alert the user about all the events on the editing page
		editMessageSection = ttk.Frame(self.editPage)
		editMessageSection.pack(pady=10)
		self.editMessageLabel = ttk.Label(editMessageSection, text="")
		self.editMessageLabel.grid(row=0, column=0)

		# Create section for inputting information about editing accounts and create a section for buttons 
		inputEditSection = ttk.LabelFrame(self.editPage, text="Edit Account Information")
		inputEditSection.pack(ipadx=20, ipady=10)
		
		# Create button section for edit page
		editBtnSection = ttk.Frame(inputEditSection)
		
		# Create buttons for editBtnSection; this will be the button to confirm edits on the user's account
		# Then the openChangePasswordButton will open the page to change the user's password
		confirmEditBtn = ttk.Button(editBtnSection, text="Confirm Edits", command=self.editUserAccount)		
		openChangePasswordBtn = ttk.Button(editBtnSection, text="Change Password", command=lambda: self.master.openPage("userChangePassword"))
		
		# Position your buttons
		confirmEditBtn.grid(row=0, column=0, padx=10, pady=10)
		openChangePasswordBtn.grid(row=0, column=1, padx=10, pady=10)

		# Field names that will be edited; 
		fieldNamesEdit = ["Username", "First Name", "Last Name", "Email", "Shipping Address"]
		self.entryEditList = []

		# Create labels and entry widgets and then finally position the editBtnSection at the bottom of the grid
		# Then fill out the entry widgets with the current information from the user's account
		# Store the entry widgets for later
		for x in range(len(fieldNamesEdit)):
			fieldLabelEdit = ttk.Label(inputEditSection, text=f"{fieldNamesEdit[x]}:")
			fieldEntryEdit = ttk.Entry(inputEditSection)
			fieldEntryEdit.insert(0, self.master.loggedinUser.getAttributeByName(fieldNamesEdit[x]))
			fieldLabelEdit.grid(row=x, column=0, padx=5, pady=10)
			fieldEntryEdit.grid(row=x, column=1, padx=5, pady=10)
			self.entryEditList.append(fieldEntryEdit)

		# Position the button section for the edits and position the buttons as well
		editBtnSection.grid(row=len(fieldNamesEdit), column=0, columnspan=2)
		confirmEditBtn.grid(row=0, column=0)
		openChangePasswordBtn.grid(row=0, column=1)

	## Function checks user accounts and then goes to make edits in the database if successful
	def editUserAccount(self):
		# Input validation to check if entry widgets are empty; if user only entered spaces, then an empty string woudl be the result
		self.entryEditList = Utilities.stripEntryWidgets(self.entryEditList)

		# Since whitespace was already stripped, if any of the inputs are empty strings, they left it blank
		if Utilities.isEmptyEntryWidgets(self.entryEditList):
			self.editMessageLabel.config(text="Account Edit Error: Some fields were left blank")
			return
		
		with self.master.conn:
			self.master.cursor.execute(f"SELECT id FROM Users WHERE username=:username", {"username": self.entryEditList[0].get().strip()})
			data = self.master.cursor.fetchone()
			# If a usernames from the database is found, then it could be a duplicate or it could be the user's own username we are matching
			# If it's another account that has the username, then it's a duplicate username and we throw an error
			if data is not None and data[0] != self.master.loggedinUser.getID():
				self.editMessageLabel.config(text= "Username is already taken")
				return
			# If these tests are passed then we should save the stuff in the database
			# .strip() to remove any leading or trailing whitespace in the user's input
			self.master.cursor.execute(f'''UPDATE Users SET username=:username, fname=:fname, lname=:lname, email=:email, address=:address WHERE id=:id''', 
		    {
				"username": self.entryEditList[0].get(),
				"fname": self.entryEditList[1].get(),
				"lname": self.entryEditList[2].get(),
				"email": self.entryEditList[3].get(),
				"address": self.entryEditList[4].get(),
				"id": self.master.loggedinUser.getID()
			})

			# Select a User from the User table and update the current logged in user
			self.master.cursor.execute(f"SELECT * FROM Users WHERE id=:id", {"id": self.master.loggedinUser.getID()})
			data = self.master.cursor.fetchone()
			self.master.loggedinUser =  User(data[0], data[1], data[2], data[3], data[6], data[9], data[4], data[7], data[5])

			

			



		# update the loggedinUser class instance

		# After they change their password, we log them out of their account. 
		self.master.openPage("userPage")
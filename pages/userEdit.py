import tkinter as tk
from tkinter import ttk
from classes.User import User
import classes.utilities as Utilities

# Class or page for editing the current user's account; for changing account information such as name, email, etc.
# NOTE: Page will link to pages for changing the user's password and managing the user's wallet
class userEdit(tk.Frame): 
	def __init__(self, master, app, currentUser):
		super().__init__(master)
		self.app = app
		self.master = master

		# User class instance representing the currently logged in user, passed from userPage
		self.currentUser = currentUser

		# Create the frame that contains all the widgets and elements on the editPage
		self.editPage = ttk.Frame(self)
		self.editPage.pack(expand=True)
		
		# Create message section that will alert the user about all the events on the editing page
		self.editMessageSection = ttk.Frame(self.editPage)
		self.editMessageLabel = ttk.Label(self.editMessageSection, text="")
		self.editMessageSection.pack(pady=10)
		self.editMessageLabel.grid(row=0, column=0)

		# Create section for inputting information about editing accounts and create a section for buttons 
		self.inputEditSection = ttk.LabelFrame(self.editPage, text="Edit Account Information")
		self.inputEditSection.pack(ipadx=20, ipady=10)
		
		# Create button section for edit page
		self.editBtnSection = ttk.Frame(self.inputEditSection)
		
		# Create buttons for editBtnSection; this will be the button to confirm edits on the user's account
		# Then the openChangePasswordButton will open the page to change the user's password
		self.confirmEditBtn = ttk.Button(self.editBtnSection, text="Confirm Edits", command=self.editUserAccount)		
		self.openChangePasswordBtn = ttk.Button(self.editBtnSection, text="Change Password", command=lambda: self.master.openPage("userChangePassword"))
		
		# Position your buttons
		self.confirmEditBtn.grid(row=0, column=0, padx=10, pady=10)
		self.openChangePasswordBtn.grid(row=0, column=1, padx=10, pady=10)

		# Field names that will be edited; 
		self.fieldNamesEdit = ["Username", "First Name", "Last Name", "Email", "Shipping Address"]
		self.entryEditList = []

		# Create labels and entry widgets and then finally position the editBtnSection at the bottom of the grid
		# Then fill out the entry widgets with the current information from the user's account
		# Store the entry widgets for later
		for x in range(len(self.fieldNamesEdit)):
			fieldLabelEdit = ttk.Label(self.inputEditSection, text=f"{self.fieldNamesEdit[x]}:")
			fieldEntryEdit = ttk.Entry(self.inputEditSection)
			fieldEntryEdit.insert(0, self.currentUser.getAttributeByName(self.fieldNamesEdit[x]))
			fieldLabelEdit.grid(row=x, column=0, padx=5, pady=10)
			fieldEntryEdit.grid(row=x, column=1, padx=5, pady=10)
			self.entryEditList.append(fieldEntryEdit)

		# Position the button section for the edits and position the buttons as well
		self.editBtnSection.grid(row=len(self.fieldNamesEdit), column=0, columnspan=2)
		self.confirmEditBtn.grid(row=0, column=0)
		self.openChangePasswordBtn.grid(row=0, column=1)

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
			if data is not None and data[0] != self.master.loggedinUser:
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
				"id": self.master.loggedinUser
			})

		# After they change their password, we log them out of their account. 

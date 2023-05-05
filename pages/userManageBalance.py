import tkinter as tk
from tkinter import ttk
from classes.User import User
import classes.utilities as Utilities
import locale

class userManageBalance(tk.Frame):
	def __init__(self, master, app):
		super().__init__(master)
		self.master = master
		self.app = app

		locale.setlocale(locale.LC_ALL, '')

		# User class representing the currently logged in user, passed from userPage 
		self.currentUser = self.master.loggedinUser


		# Create a frame where all of the balance information information will be 
		self.balancePage = ttk.Frame(self)
		self.balancePage.pack(expand=True)
		
		# Creation section and label for showing the user events on the page for managing their balance
		self.balanceMessageSection = ttk.Frame(self.balancePage)
		self.balanceMessageLabel = ttk.Label(self.balanceMessageSection, text="")
		self.balanceMessageSection.pack(pady=10)
		self.balanceMessageLabel.grid(row=0, column=0)

		# Section for inputting the balance information and showing balance info 
		self.inputBalanceSection = ttk.LabelFrame(self.balancePage, text="Balance info")
		self.inputBalanceSection.pack(ipadx=20, ipady=10)

		# Section for containing buttons for the balance page
		self.balanceBtnSection = ttk.Frame(self.inputBalanceSection)

		# Two types of fields that relate to "balance" and money. However user will not be able to influence "points"
		# NOTE: List will only be used for making labels in balanceInfoSection; label and entry widget for input will be done separately
		self.fieldNamesBalance = ["Balance", "Points"]
		
		# Create the point and balance label; the balance label will be updated when the user updates their balance on the page
		self.userBalanceLabel = ttk.Label(self.inputBalanceSection, text=f"{self.fieldNamesBalance[0]}: {self.currentUser.getAttributeByName(self.fieldNamesBalance[0])}")
		self.userPointsLabel = ttk.Label(self.inputBalanceSection, text=f"{self.fieldNamesBalance[1]}: {self.currentUser.getAttributeByName(self.fieldNamesBalance[1])}")
		self.userPointsLabel.grid(row=0, column=0)
		self.userBalanceLabel.grid(row=1, column=0)

		# Create label and entry widget for input balance section; then psoition the balance button section below it
		self.fieldBalanceLabel = ttk.Label(self.inputBalanceSection, text="Amount:")
		self.fieldBalanceEntry = ttk.Entry(self.inputBalanceSection)
		self.fieldBalanceLabel.grid(row=len(self.fieldNamesBalance), column=0, padx=5, pady=10)
		self.fieldBalanceEntry.grid(row=len(self.fieldNamesBalance), column=1, padx=5, pady=10) 
		self.balanceBtnSection.grid(row=len(self.fieldNamesBalance) + 1, column=0, columnspan=2, sticky=tk.S)

		# Create buttons, so that user can add or subtract a certain balance from their total balance
		self.addBalanceBtn = ttk.Button(self.balanceBtnSection, text="Add Balance", command=lambda: self.updateBalance("ADD"))
		self.subtractBalanceBtn = ttk.Button(self.balanceBtnSection, text="Subtract Balance", command=lambda: self.updateBalance("SUBTRACT"))
		self.addBalanceBtn.grid(row=0, column=0, padx=5, pady=10)
		self.subtractBalanceBtn.grid(row=0, column=1, padx=5, pady=10)


	## Updates the balance label in the inputBalanceSection
	def updateBalanceLabel(self):	
		self.userBalanceLabel.config(text=f"Balance: {locale.currency(self.currentUser.getBalance())}")

	## Calculates new balance for user in regards to the amount they put in and what operation they did
	## It then updates that balance in the database, and then updates that value in currentUser instance so that we can easily update labels without
	## Having to access the database again.
	def updateBalance(self, operation):
		# inputAmount represents numerical amount of money the user inputted in the entry widget
		inputAmount = self.fieldBalanceEntry.get().strip()

		# Check if amount field was left blank
		if inputAmount == "":
			self.balanceMessageLabel.config(text="Amount field was left blank")
			return
		# First check whether they inputted a valid numerical input doing a try/except. If it isn't a 
		# valid number input then return an exception and tell the user
		try:
			# Convert user input into a number
			# If they input a number such as "23.412" we will ensure that it's in dollars and cents always
			inputAmount = float(inputAmount)
			inputAmount = round(inputAmount, 2) 
		except ValueError:
			self.balanceMessageLabel.config(text="Please enter a valid numerical input for the amount")
			return
		# Now check whether that input is a positive number, The user should be able to enter anything less than 0
		if inputAmount <= 0:
			self.balanceMessageLabel.config(text="Please enter a value greater than 0")
			return
		
		# Now they've got a valid number they can add to their balance, we can update their balances
		newBalance = self.currentUser.getBalance()

		# Calculate the new total balance of the user 
		if operation == "ADD":
			newBalance += inputAmount
		else:
			# Else they want to subtract from their balance
			# Before we do that we need to check their balance isn't going to go below 0 if they subtract from their balance
			if newBalance - inputAmount < 0:
				self.balanceMessageLabel.config(text="Balance Error: Subtracted amount is more than you have in your account")
				return
			newBalance -= inputAmount
		
		# Then update their balance in the database in the database
		with self.master.conn:
			self.master.cursor.execute("UPDATE Users SET balance=:balance WHERE id=:id", 
			{
				"balance": newBalance,
				"id": self.master.loggedinUser
			})
		# update the balance for the current user, which we can then use to update the balance label
		self.currentUser.setUserBalance(newBalance)

		# Now that we have our new balance, we should update the balance label 
		self.updateBalanceLabel()
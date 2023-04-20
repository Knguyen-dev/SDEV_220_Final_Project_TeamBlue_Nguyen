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
 

class registerUserAccount(tk.Frame):
	# self is own frame, master main file, app is the window
	def __init__(self, master, app):
		super().__init__(master)


		self.app = app
		self.registrationPage = tkb.Frame(self)
		self.registrationPage.pack(expand=True)

		# Create the login section where you input the information
		self.inputCreationSection = tkb.LabelFrame(self.registrationPage, text="Enter credentials to log in")
		self.inputCreationSection.pack(fill=BOTH, expand=True, ipadx=20, ipady=10)

		self.createBtnSection = tkb.Frame(self.inputCreationSection)

		self.fieldNamesCreate = ["Username", "First Name", "Last Name", "Shipping Address", "Email", "Password", "Retype Password"] # List of fields names needed for logging
		self.entryCreateList = [] # List of entry widgets for getting login input, we will then access these widgets later in the loginUserAccount function


		# Create label and entry widgets for each field, and position them; store the entry widgets for later use
		for x in range(len(self.fieldNamesCreate)):
			fieldLabelCreate = tkb.Label(self.inputCreationSection, text=f"{self.fieldNamesCreate[x]}:")
			fieldEntryCreate = tkb.Entry(self.inputCreationSection)
			fieldLabelCreate.grid(row=x, column=0, padx=5, pady=5)
			fieldEntryCreate.grid(row=x, column=1, padx=5, pady=5)
			self.entryCreateList.append(fieldEntryCreate)

		self.createBtnSection.grid(row=len(self.fieldNamesCreate), column=0, columnspan=2, sticky=tk.S, padx=10)
		
		# Create a confirm log in button and close login page window; position those buttons
		
		openLoginPageBtn = tkb.Button(self.createBtnSection, text="Already have an account?", command=lambda: self.openPage("userLogin"))
		confirmCreationBtn = tkb.Button(self.createBtnSection, text="Confirm", command=self.createUserAccount)
		openLoginPageBtn.grid(row=len(self.fieldNamesCreate), column=0, padx=10, pady=10)
		confirmCreationBtn.grid(row=len(self.fieldNamesCreate), column=1, padx=10, pady=10)

		

	
	def createUserAccount(self):
		for entry in self.entryCreateList:
			print(entry.get())





			



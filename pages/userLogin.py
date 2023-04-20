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
 

class userLogin(tk.Frame):
	# self is own frame, master main file, app is the window
	def __init__(self, master, app):
		super().__init__(master)

		self.app = app
		self.loginPage = tk.Frame(self)
		self.loginPage.pack(expand=True)

		# Create the login section where you input the information
		self.inputLoginSection = tk.LabelFrame(self.loginPage, text="Enter credentials to log in")
		self.inputLoginSection.pack(fill=BOTH, expand=True, ipadx=20, ipady=10)

		self.loginBtnSection = tkb.Frame(self.inputLoginSection)

		self.fieldNamesLogin = ["Email", "Password"] # List of fields names needed for logging
		self.entryLoginList = [] # List of entry widgets for getting login input, we will then access these widgets later in the loginUserAccount function


		# Create label and entry widgets for each field, and position them; store the entry widgets for later use
		for x in range(len(self.fieldNamesLogin)):
			fieldLabelLogin = tkb.Label(self.inputLoginSection, text=f"{self.fieldNamesLogin[x]}:")
			fieldEntryLogin = tkb.Entry(self.inputLoginSection)
			fieldLabelLogin.grid(row=x, column=0, padx=5, pady=10, ipadx=20)
			fieldEntryLogin.grid(row=x, column=1, padx=5, pady=10, ipadx=20)
			self.entryLoginList.append(fieldEntryLogin)
		
		self.loginBtnSection.grid(row=len(self.fieldNamesLogin), column=0, columnspan=2, sticky=tk.S)

		# Create a confirm log in button and close login page window; position those buttons		
		openCreateAccountBtn = tkb.Button(self.loginBtnSection, text="Don't have an account?", command=lambda: self.master.openPage("registerUserAccount"))
		confirmLoginBtn = tkb.Button(self.loginBtnSection, text="Confirm", command=self.loginUserAccount)
		openCreateAccountBtn.grid(row=len(self.fieldNamesLogin), column=0, padx=10, pady=10)
		confirmLoginBtn.grid(row=len(self.fieldNamesLogin), column=1, padx=10, pady=10)

	
	def loginUserAccount(self):
		for entry in self.entryLoginList:
			print(entry.get())

		# print(hashlib.md5('password'))





			



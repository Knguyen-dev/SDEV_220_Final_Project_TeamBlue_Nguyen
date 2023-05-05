import importlib
import sqlite3
## Tkinter and Tkinter Framework
import tkinter as tk
from tkinter import ttk
from classes.ShoppingCart import *
from classes.User import *


class App(tk.Tk):
	def __init__(self):
		super().__init__()
		self.title("Kroger")
		width = self.winfo_screenwidth()
		height = self.winfo_screenheight()
		self.geometry("%dx%d" % (width, height))
		self.conn = sqlite3.connect('assets/PyProject.db')
		self.cursor = self.conn.cursor()
		self.loggedinUser = None
		# This is where the magic happens
		self.tk.call("source", "azure.tcl")
		self.tk.call("set_theme", "dark")
		self.CartClass = ShoppingCart()
		self.createNavbar()
		self.current_page = None      

		self.bind('<Return>', self.searchFunction)
		self.openPage("homePage")

	## function: loadPage(page_name: str)
	## This function is called to check if a class exists inside the pages directory
	## if the page exists, it imports the page class and returns it to the caller.
	def loadPage(self, page_name):
		try:
			# import the module using the full path
			module = importlib.import_module(f"pages.{page_name}")
			# get the page class from the module
			page_class = getattr(module, page_name)
			return page_class
		except (ImportError, AttributeError):
			print(f"Error: Page {page_name} does not exist.")
			return None

	## function: openPage(page_name: str, *args: any)
	## This function is called to open a new page, It imports the page class using load_page,
	## If the page exists it destroys the current and replaces with new page class
	def openPage(self, page_name, *args):
		page_class = self.loadPage(page_name)
		if page_class is None:
			return

		if self.current_page:
			self.current_page.destroy()

		self.current_page = page_class(self, self, *args) 
		self.current_page.pack(fill='both', expand=True)

	## function createNavbar()
	## Creates the navbar and all respective buttons
	def createNavbar(self):
		# create the top menu
		self.navbar = ttk.Frame(self)
		self.navbar.pack(fill="x", ipady=10, side="top")

		#logo frame
		self.logoFrame = ttk.Frame(self.navbar)
		self.logoFrame.pack(fill="y", side="left")
		#logo
		self.logo = ttk.Button(self.logoFrame, width=10, text="Kroger", command=lambda: self.openPage("homePage"))
		self.logo.pack(side="left", ipady=8, padx=2)

		# Search frame
		self.searchFrame = ttk.Frame(self.navbar)
		self.searchFrame.pack(fill="y", side="left")
		# Search bar and button
		self.searchBar = ttk.Entry(self.searchFrame, width=140)
		self.searchBar.pack(side="left", ipady=8, padx=2, anchor="center") 
		self.searchButton = ttk.Button(master=self.searchFrame, text='Search', compound="right", command= lambda: self.openPage("homePage", self.searchBar.get()))
		self.searchButton.pack(fill="y", side="right")

		# user frame
		self.userFrame = ttk.Frame(self.navbar)
		self.userFrame.pack(fill="y", side="right")
		# user / cart button
		self.cartButton = ttk.Button(master=self.userFrame, text='Cart', compound="right", command=lambda: self.openPage("cartPage"))
		self.cartButton.pack(side="left", ipadx=10, fill="y")

		# create the userButton; by default it's set to "Login" and takes you to the login page, but once you log in, it changes to show your account
		# NOTE: Logic for changing the button is in the userLogin page 
		self.userButton = ttk.Button(master=self.userFrame, text='Login', compound="right", command=lambda: self.openPage("userLogin"))
		self.userButton.pack(side="left", ipadx=10, fill="y")
		
		

	## function searchFunction()
	## Grabs text from inside of searchBar Entry and sends data to homePage
	def searchFunction(self, e=None):
		if self.focus_get() == self.searchBar:
			self.openPage("homePage", self.searchBar.get())

	## Logs out the user by clearing the loggedinUser variable, and taking user to the login page
	# NOTE: Put in main since it's needed in both userPage and userChangePassword
	def logOutUser(self):
		self.loggedinUser = None
		self.CartClass.emptyShoppingCart()
		# Change userButton so that it redirects to the login page 
		self.userButton.configure(text="Login", command=lambda: self.openPage("userLogin"))
		self.openPage("userLogin")
		return
	
	## Cart Manager Function
	def handleCart(self, action, product=None):
		if action == "add":
			print("something")
		elif action == "remove":
			print("remove")
		elif action == "edit":
			self.cart[product]


if __name__ == "__main__":
    app = App()
    app.mainloop()

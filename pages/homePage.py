from threading import Thread
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import sqlite3

# Home page class
class homePage(tk.Frame):
	# master: Calls back to parent class
	# app: Main tkinter window for the whole application
	# args: Products they wanted  to search for
	def __init__(self, master, app, *args):
		super().__init__(master)
		self.master = master
		self.app = app
		## homePage Frame to make page responsive
		# Actually a giant text box with a lot of whitespace so that our product cards can go on there. We put it in a state of disabled so that
		# The user doesn't accidentally type on it, with it being a text box
		self.homePage = tk.Text(self, bd = 10, wrap="char", borderwidth=1, highlightthickness=0, state="disabled", spacing1 = 50, spacing2 = 20, insertofftime=0, cursor="arrow")
		self.homePage.pack(fill='both', expand=True)

		## Database variables
		self.conn = sqlite3.connect('assets/PyProject.db')
		self.cursor = self.conn.cursor()
		self.homePage.tag_configure("center", justify='center') 
		## For searchbar if search is empty dont call searchProducts()
		if args:
			if args[0] is not None:
				self.searchProducts(args[0])
		else:
			self.getProducts()
			
		self.homePage.tag_add("center", 1.0, "end")

	# Creates product "cards" or "sections" for "product" which is an sqlite row entry
	def createProductDisplay(self, product):
		# Represents product card, main card
		product_card = ttk.Frame(self.homePage, width=200, height=200, relief="solid", padding=10)

		# Image section
		imageFrame = ttk.Frame(product_card, height=120)

		# Opens url, reads image data, create and resize our image; format it with tkinter and position on screen 
		image = Image.open(product[4])
		image = image.resize((120, 120))
		image = ImageTk.PhotoImage(image=image)
		image_label = ttk.Label(imageFrame, image=image)
		image_label.image = image
		image_label.grid(row=0, column=0, sticky=tk.EW, padx=3, pady=3)
		imageFrame.pack(fill='x')

		# Represents the detail section of the product card; item name, price, buttons, etc.
		# Below are corresponding labels and widgest for this section
		detailFrame = ttk.Frame(product_card, height=80)

		price_label = ttk.Label(detailFrame, text=f"$ {product[2]}", font=("Helvetica", 10), width=40, anchor="w")
		price_label.grid(row=1, column=0, sticky=tk.NSEW)

		# if the user is logged in (loggedinUser isn't none), then let them add stuff to the cart
		# However if the user isn't logged in, then when they try to press the buy button, just take them to the login page
		if self.master.loggedinUser == None:
			buyButton = ttk.Button(detailFrame, text="Add to cart", command=lambda: self.master.openPage("userLogin"))
		else:
			buyButton = ttk.Button(detailFrame, text="Add to cart", command= lambda: self.master.CartClass.updateCartItem(product, 1))
		buyButton.grid(row=1, column=1, sticky=tk.NS)

		name_label = ttk.Label(detailFrame, text=product[1], font=("Helvetica", 10, 'bold'), width=40, anchor="w")
		name_label.grid(row=0, column=0, sticky=tk.NSEW)

		# Assign a command to the name label so that it calls function when user presses it
		name_label.bind("<Button-1>", lambda e:self.master.openPage("productPage", product[0]))
		detailFrame.pack(fill='x', expand=True)
		
		## Changes state of homePage to Normal to allow the insertation of product card, then changes back to disabled
		self.homePage.configure(state="normal")

		# Inserts the product cards as a window
		self.homePage.window_create("end", window=product_card)

		# Change the homePage textbox back to disabled so no accidentally typing on it
		self.homePage.configure(state="disabled")

	# create threads for making product displays
	def thread(self, row):
		t1=Thread(target=self.createProductDisplay(row))
		t1.start()

	# Searches for specific items in the database, then calls function so that they are processed for creating image cards
	def searchProducts(self, searchedProduct):
		self.cursor.execute("SELECT * FROM items WHERE name LIKE ? LIMIT 12", ('%' + searchedProduct + '%',))
		rows = self.cursor.fetchall()
		if len(rows) > 0:
			for row in rows:
				self.thread(row)
		else:
			self.emptyLabel = ttk.Label(self.homePage, text="Nothing was found.")
			self.emptyLabel.pack()

	# Same thing as above function, but for all products
	def getProducts(self):
		self.cursor.execute("SELECT * FROM items LIMIT 12")
		rows = self.cursor.fetchall()
		for row in rows:
			self.thread(row)
		
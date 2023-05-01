import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from urllib.request import urlopen
import io
from classes.User import User
import locale

# Class represents the userPage or my account page. To get to this page the user should go through the login process first, which 
# ensures that an account exists to create this page for.
class userPage(tk.Frame):
	def __init__(self, master, app, userID):
		super().__init__(master)
		self.master = master
		self.app = app
		
		# Create the frame where all of the user information will lay
		self.userPage = ttk.Frame(self)
		self.userPage.pack(fill='both', expand=True)
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
		self.userAttributeNames = ["Username", "Email", "Shipping Address", "Balance", "Points"]

		# Call functions that create image and user frames that lay on userPage in a grid
		self.createImageFrame() # row = 0, col = 0
		self.createUserFrame() # row = 0, col = 1
		self.createProfileBtnsSection() # row = 1, col = 0
		self.createRecentPurchasesSection() # row = 1, col = 1

	# Create an edit profile button that takes them to the edit account page and position it
	def createProfileBtnsSection(self):
		# Create section for containing buttons to manage your account
		self.profileBtnsSection = ttk.Frame(self.userPage)
		self.profileBtnsSection.grid(row=1, column=0)
		# Create and position buttons for the profileBtnsSection
		self.openEditAccountBtn = ttk.Button(self.profileBtnsSection, text="Edit Account", command=lambda: self.master.openPage("userEdit", self.currentUser))
		self.openManageBalanceBtn = ttk.Button(self.profileBtnsSection, text="Manage Wallet", command=lambda: self.master.openPage("userManageBalance", self.currentUser))
		self.logOutBtn = ttk.Button(self.profileBtnsSection, text="Log out", command=self.master.logOutUser)
		self.openDeleteAccountBtn = ttk.Button(self.profileBtnsSection, text="Delete Account", command=lambda: self.master.openPage("userDelete"))
		self.openEditAccountBtn.grid(row=0, column=0, padx=5, pady=5)
		self.openManageBalanceBtn.grid(row=1, column=0, padx=5, pady=5)
		self.logOutBtn.grid(row=2, column=0, padx=5, pady=5)
		self.openDeleteAccountBtn.grid(row=3, column=0, padx=5, pady=5)

	## Function creates section for recent purchases 
	def createRecentPurchasesSection(self):
		# Create section or frame for recent purchases and position it
		self.recentPurchasesSection = ttk.Frame(self.userPage)
		self.recentPurchasesSection.grid(row=1, column=1, ipadx=20, ipady=20)

		# Title or header for the recent purchases section
		sectionTitle = ttk.Label(self.recentPurchasesSection, text="Your Recent Purchases", font=("Helvetica", 18, "bold"))
		sectionTitle.pack()

		# Create section or frame where we store the recent purchase labels and info like a list
		self.purchaseListSection = ttk.Frame(self.recentPurchasesSection)
		self.purchaseListSection.pack(ipadx=20, ipady=20) 

		# Query for 3 of the most recent purchases made my the user; query using the user's id and selecting from the order
		# NOTE: For this example, we filled 3 "orders" outs in the Orders table to help visualize this process;
		with self.master.conn:

			# From the Orders table, we are going to flip and query the table in descending order by the id or primary keys
			# This is just another way to get maybe the top three most recent purchases by the user
			self.master.cursor.execute("SELECT * FROM Orders ORDER BY id DESC LIMIT 3")
			recentPurchases = self.master.cursor.fetchall()

			# Create labels and buttons associated with each purchase and position it
			for x in range(len(recentPurchases)):
				purchaseLabel = ttk.Label(self.purchaseListSection, text=f"Purchase ID: {recentPurchases[x][0]} - Total Quantity: {recentPurchases[x][3]} - Total Cost: {locale.currency(recentPurchases[x][1])}", font=("Helvetica", 12, "bold"))
				purchaseInfoBtn = ttk.Button(self.purchaseListSection, text="More Info")
				purchaseLabel.grid(row=x, column=0, padx=5, pady=5, sticky="w")
				purchaseInfoBtn.grid(row=x, column=1, padx=5, pady=5, sticky="e")

	## Create frame or section to show user information 
	def createUserFrame(self):
		# Create main section for all user information 
		self.userDetailsSection = tk.Canvas(self.userPage, width=100)
		# Create section for show user account or user instance attributes
		self.userInfoSection = ttk.Frame(self.userDetailsSection)

		# Put all labels in userInfoSection
		# Create username label, make it big and visible since for aesthetic purposes
		usernameLabel = ttk.Label(self.userInfoSection, text=f"{self.currentUser.getFirstName()} {self.currentUser.getLastName()}", font=('Helvetica', 32, 'bold'))
		usernameLabel.grid(row=0, column=0, columnspan=3, padx=20, pady=10)

		# Create labels for the other attributes for the user; exclude username from iteration
		# We start at 1 because we want to avoid row index 0 since the username label is already occupying that entire row 
		for x in range(len(self.userAttributeNames)):
			userAttributeLabel = ttk.Label(self.userInfoSection, text=f"{self.userAttributeNames[x]}: {self.currentUser.getAttributeByName(self.userAttributeNames[x])}", font=("Helvetica", 18, "bold"))
			userAttributeLabel.grid(row=(x + 1), column=0, pady=5, sticky="w")
		# Position userDetailsSection on the userPage
		self.userInfoSection.pack(fill='x')
		self.userDetailsSection.grid(row=0, column=1, sticky=tk.N, padx=(150, 200))

	## Create frame or section to show the image or avatar of the user's account
	def createImageFrame(self):
		self.imageFrame = tk.Canvas(self.userPage, highlightbackground="#eee", highlightthickness=1)
		response = urlopen(self.userAvatarSource)
		data = response.read()
		image = Image.open(io.BytesIO(data))
		image = image.resize((350, 350))
		image = ImageTk.PhotoImage(image=image)
		image_label = ttk.Label(self.imageFrame, image=image)
		image_label.image = image
		image_label.grid(row=0, column=0, sticky=tk.EW, padx=3, pady=3)
		self.imageFrame.grid(row=0, column=0, padx=40)
	
	# Get the user information; login process guarantees that an existing and valid userID exists, so we can be sure that this query always brings the right user data
	def getUser(self, id):
		self.master.cursor.execute(f"SELECT * FROM Users WHERE id={id}")
		user = self.master.cursor.fetchone()
		return user
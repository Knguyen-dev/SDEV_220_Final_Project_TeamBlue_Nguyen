import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from urllib.request import urlopen
import io
import locale
from classes.Purchase import *

BLUE = "#0f52a2"
PINK = "#f5f5f5"
ACCENT = "#21409A"

class cartPage(tk.Frame):
	def __init__(self, master, app):
		super().__init__(master)
		self.app = app

		# Create frame to have all of the cart item displays
		self.content = tk.Frame(self)
		self.content.pack(fill='both', expand=True)
		self.content.rowconfigure(0, weight=1) # set row 0 to expand vertically 
		locale.setlocale(locale.LC_ALL, '')
		
		# Create frames, labels, and variables for handling cart cost and totals
		# NOTE: Subtotal and tax are kept as numbers for calculations at the end, whilst totalVar is for display purposes which is why it's the only one with locale.currency
		self.subTotalVar = tk.DoubleVar(value=round((self.master.CartClass.getTotalCost()), 2))
		self.taxVar = tk.DoubleVar(value=round((self.subTotalVar.get() * 0.07), 2))
		self.totalVar = tk.DoubleVar(value=locale.currency(self.subTotalVar.get() + self.taxVar.get()))

		# Create section to contain subtotal, tax, total, checkout, and other widgets
		self.orderFrame = tk.Frame(self.content, width=700)
		self.orderFrame.pack(fill='y', padx=(100, 0), pady=10, ipadx=50, side='right', expand=False)		
		self.OrderFrameLabel = ttk.Label(self.orderFrame, text="Order Summary", font=("Helvetica", 18, 'bold'), anchor="e")
		self.OrderFrameLabel.grid(row=0, column=0, columnspan=2)
		
		self.subtotalLabel = ttk.Label(self.orderFrame, text="Subtotal: ", font=("Helvetica", 14), anchor="e")
		self.subtotalLabel.grid(row=1, column=0)
		self.subtotalNumber = ttk.Label(self.orderFrame, textvariable=self.subTotalVar, font=("Helvetica", 14), anchor="e")
		self.subtotalNumber.grid(row=1, column=1)
		
		self.taxLabel = ttk.Label(self.orderFrame, text="Tax: ", font=("Helvetica", 14), anchor="e")
		self.taxLabel.grid(row=2, column=0)
		self.taxNumber = ttk.Label(self.orderFrame, textvariable=self.taxVar, font=("Helvetica", 14), anchor="e")
		self.taxNumber.grid(row=2, column=1)
		
		self.totalLabel = ttk.Label(self.orderFrame, text="Total: ", font=("Helvetica", 14), anchor="e")
		self.totalLabel.grid(row=3, column=0)
		self.totalNumber = ttk.Label(self.orderFrame, textvariable=self.totalVar, font=("Helvetica", 14), anchor="e")
		self.totalNumber.grid(row=3, column=1)

		# Create button for checking out item
		checkOutPurchaseBtn = ttk.Button(self.orderFrame, text="Check out", command=self.purchaseItems)
		checkOutPurchaseBtn.grid(row=4, column=0, columnspan=2, pady=15)

		# Section for showing events on the cart page; and label that will show messages 
		cartMessageSection = ttk.Frame(self.orderFrame)
		cartMessageSection.grid(row=5, column=0, columnspan=2)
		self.cartMessageLabel = ttk.Label(cartMessageSection, text="", font=("Helvetica", 10, 'bold'))
		self.cartMessageLabel.grid(row=0, column=0)
		
		# Create section for having a picture/graphic
		self.canvas = tk.Canvas(self.content, width=250, height=700)
		self.character_img = tk.PhotoImage(file='images/bagMan.png')
		self.canvas.create_image(190,475, image=self.character_img)
		self.bubble_img = tk.PhotoImage(file='images/bubbleText.png')
		self.canvas.create_image(140,140, image=self.bubble_img)
		self.canvas.pack(fill='both', expand=True, side='left')

		# Label to indicate where user items will appear
		cart_label = ttk.Label(self.content, text="Your Items", font=("Helvetica", 14, 'bold'), width=60)
		cart_label.pack(fill='x', ipady=40, side='top')

		# Get cart items cart class
		self.cart = self.master.CartClass.getCartItems()

		# Create dictionary for handling the items and their changing quantities; helps our quantity changing functionality
		self.cartItems = dict(dict())
		
		# Render their shopping cart items with a function
		for item in self.cart:
			self.createCartDisplay(item[0], item[1])


	# Creates the display for the cart item
	def createCartDisplay(self, product, quantity):
		# Create section for each item
		cartItemDisplay = tk.Frame(self.content)
		# Create image
		imageFrame = tk.Frame(cartItemDisplay, height=80, width=80)
		image = Image.open(product[4])
		image = image.resize((120, 120))
		image = ImageTk.PhotoImage(image=image)
		image_label = ttk.Label(imageFrame, image=image)
		image_label.image = image
		image_label.grid(row=0, column=0, padx=3, pady=3)
		imageFrame.grid(row=0, column=0, padx=3, pady=3, rowspan=2)
		# Create names and description labels for item
		name_label = ttk.Label(cartItemDisplay, text=product[1], font=("Helvetica", 10, 'bold'), anchor="w")
		name_label.grid(row=0, column=1, sticky="n")
		descriptionLabel = ttk.Label(cartItemDisplay, text=product[3], font=("Helvetica", 10), anchor="nw")
		descriptionLabel.grid(row=1, column=1, sticky="nw")

		# Create variables for quantity and price of the item when considering quantity
		quantityVar = tk.StringVar(value = quantity) # string rep. for quantity for a given item
		totalItemPriceVar = tk.StringVar(value = locale.currency(product[2] * quantity)) # total price/cost considering quantity for that item

		# Create label for showing the total cost of the item
		totalItemPriceLabel = ttk.Label(cartItemDisplay, textvariable=totalItemPriceVar, font=("Helvetica", 14, 'bold'), width=20, anchor="e")
		totalItemPriceLabel.grid(row=2, column=1, sticky="e")

		# Create section to contain the buttons and text for changing the quantities of the item
		incrementerFrame = ttk.Frame(cartItemDisplay)
		decrementButton = ttk.Button(incrementerFrame,  text=" - ", command= lambda: self.decrementItemQuantity(product), width=5)
		decrementButton.grid(row=0, column=0)
		quantityText = ttk.Entry(incrementerFrame, textvariable=quantityVar, width=8)
		quantityText.grid(row=0, column=1)
		incrementButton = ttk.Button(incrementerFrame,  text=" + ", command= lambda: self.incrementItemQuantity(product), width=5)
		incrementButton.grid(row=0, column=2)
		incrementerFrame.grid(row=2, column=0, sticky="e")

		# Button for removing item from cart:
		removeCartItemBtn = ttk.Button(cartItemDisplay, text="Remove From Cart", command=lambda: self.removeCartItem(product, cartItemDisplay))
		removeCartItemBtn.grid(row=3, column=0, pady=10)

		# Configure column weights for column 2
		cartItemDisplay.columnconfigure(2, weight=1)
		
		# update cartItems to indicate new quantity and price
		self.cartItems.update({product[0] : {'quantity': quantityVar, 'price': totalItemPriceVar}})

		# cartItem in form of {productID:  {quantityVar : IntVar(), totalItemPriceVar : StringVar()}}
		cartItemDisplay.pack(fill='x', ipady=10, side='top')

	# Removes item from cart
	def removeCartItem(self, product, cartItemDisplay):
		# Visually remove it from self.content frame
		cartItemDisplay.pack_forget()
		# Remove it from the self.cartItems
		del self.cartItems[product[0]]
		# Then finally remove it from the cartClass itself
		self.master.CartClass.removeCartItem(product)		
		# update the price now that they removed something from the cart
		self.updateSummary()

	# Adds quantity of item by 1
	def incrementItemQuantity(self, product):
		# Get the productID and price from the product object
		productID = product[0]
		price = product[2]
		# Get the quantity from the inside dictionary of the cartItem using the productID key
		# The 'quantity' key is paired with an IntVar() value, so use .get() to get the value as an integer
		quantity = int(self.cartItems.get(productID)['quantity'].get())
		quantity = quantity + 1
		# Do the same with price, but set the value
		self.cartItems.get(productID)['price'].set(locale.currency((quantity * price)))
		# Update the quantity after it is all done
		self.cartItems.get(productID)['quantity'].set(quantity)
		# Update Cart Class with new Quantity
		self.master.CartClass.updateCartItem(product, quantity)
		## Update the cost of totalCost
		self.updateSummary()
		return
	
	# Subtracts quantity of item
	def decrementItemQuantity(self, product):
		productID = product[0]
		price = product[2]
		quantity = int(self.cartItems.get(productID).get('quantity').get())
		# If quantity is equal to one, they shouldn't be able to decrement the quantity to zero because we will have functionality get rid of the item. 
		if quantity == 1:
			return
		quantity = quantity - 1
		self.cartItems.get(productID).get('price').set(locale.currency((quantity * price)))
		self.cartItems.get(productID).get('quantity').set(quantity)
		self.master.CartClass.updateCartItem(product, quantity)
		self.updateSummary()
		return
	
	# Updates the totals when the user manipulates the quantities of items
	def updateSummary(self):
		self.subTotalVar.set(round(self.master.CartClass.getTotalCost(), 2))
		self.taxVar.set(round((self.subTotalVar.get() * 0.07), 2))
		self.totalVar.set(locale.currency(round((self.subTotalVar.get() + self.taxVar.get()), 2)))

	# Function checks out the user's shopping cart; letting them buy thier items
	def purchaseItems(self):
		# User shouldn't be able to check out nothing, so if total is zero or quantity is zero then we shuold show an error message or something
		# If there are no items in the shopping cart
		if len(self.master.CartClass.getCartItems()) == 0:
			self.cartMessageLabel.config(text="No items to checkout!")
			return

		# Get the total of the shopping cart, and get the balance of the user
		# NOTE: Rounding errors are rare but can happen it looks like despite us rounding to 2 every time, so we put this round(num, 2) for one last check
		total = round(self.subTotalVar.get() + self.taxVar.get(), 2)
		balance = self.master.loggedinUser.getBalance()

		# Gets cart items and sums up the total quantity of items
		cartItems = self.master.CartClass.getCartItems()
		totalQuantity = 0
		for item in cartItems:
			totalQuantity += item[1]
		
		# If they have enough money and it's a successful purchase
		if (balance - total) >= 0:
			# Changes user's balance and points; the point system is having 5% of the total be the amount of points they earn
			# Then save their new balance and points in the database, because I don't it has been done yet
			self.master.loggedinUser.setUserBalance((balance - total))
			currentPoints = self.master.loggedinUser.getPoints()
			earnedPoints = int(total * 0.05)
			self.master.loggedinUser.setUserPoints(currentPoints + earnedPoints)

			# Makes purchase and puts it into database
			Purchase(self.master.loggedinUser.getID(), total, totalQuantity)

			with self.master.conn:
				# Update the loggedinUser's balance and points in the database 
				self.master.cursor.execute(f'''UPDATE Users SET balance=:balance, points=:points WHERE id=:id''', 
				{
					"balance": self.master.loggedinUser.getBalance(),
					"points": self.master.loggedinUser.getPoints(),
					"id": self.master.loggedinUser.getID()
				})

				# Gets the most recent purcahse from the databaseand gets the id
				self.master.cursor.execute("SELECT id FROM Orders ORDER BY id DESC LIMIT 1")
				purchaseID = self.master.cursor.fetchone()

				# For each cart item, insert it into OrderBreakdown with corresponding information
				for item in cartItems:
					self.master.cursor.execute("INSERT INTO OrderBreakdown (order_id, item_id, quantity) VALUES (:order_id, :item_id, :quantity)", 
					{
						"order_id": purchaseID[0],
						"item_id": item[0][0],
						"quantity": item[1]
					}                           
					)
			# Calls function that empties the shopping cart, since they're done with the purchase
			self.master.CartClass.emptyShoppingCart()
			self.master.openPage("receiptPage", purchaseID[0])
		else:
			# Else this means their balance wasn't sufficient enough to make the purchase
			# In this case just show an error message and stop the execution of the function there
			self.cartMessageLabel.config(text="Insufficient Balance!")
			return
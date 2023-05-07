import tkinter as tk
from tkinter import Image, ttk
from PIL import Image, ImageTk
import sqlite3
import locale


class receiptPage(tk.Frame):
	# isCheckOut: boolean representing whether user is viewing this receipt after they checked it out
	# or they are just viewing a past receipt/order
	# orderID: Represents the Order primary key from the Orders table 
	def __init__(self, master, app, orderID):
		super().__init__(master)
		self.app = app
		locale.setlocale(locale.LC_ALL, '')
		
		# Establish the order ID as an attribute so that we can use it later
		self.orderID = orderID

		# create section where we put all of the orders and page items
		self.content = tk.Frame(self)
		self.content.pack(fill='both', expand=True)
		
		# Get the order and the items they purchased from the specific order 
		self.order = self.getOrder(orderID)
		self.orderItems = self.getOrderItems(orderID)
		
		# Create header section that gives you a welcome message and then the order ID that you're currently viewing
		self.orderFrameLabel = ttk.Label(self.content, text="Order Confirmation and Receipt", font=("Helvetica", 32, 'bold'), justify="center", anchor="center")
		self.orderFrameLabel.pack(fill='both', anchor='center')

		# Create receipt section that shows all receipt information such as items that were purchased on that order, cost of order, and amount of items bought
		receiptFrame = ttk.LabelFrame(self.content, text="Receipt/Order Info:", )
		receiptFrame.pack(anchor="center", ipadx=10, ipady=10)
		

		# Should be order ID and should be placed in order frame label
		orderIDLabel = ttk.Label(receiptFrame, text=f"Order ID: {self.order[0]}", font=("Helvetica", 15, 'bold'), anchor="e")
		orderIDLabel.grid(row=0, column=0)

		# Create section for showing the orderItems, which are the items bought in the order 
		orderItemsSection = tk.Frame(receiptFrame)
		orderItemsSection.grid(row=1, column=0)

		# Create section for showing the receipt/order statistics, and place it below the ordered items
		orderStatsSection = tk.Frame(receiptFrame)
		orderStatsSection.grid(row=2, column=0)

		# Create labels for total quantity and cost, then position them
		totalQuantityLabel = ttk.Label(orderStatsSection, text=f"Total Items: {self.order[3]}", font=("Helvetica", 12, "bold"))
		totalQuantityLabel.grid(row=0, column=0)

		totalCostLabel = ttk.Label(orderStatsSection, text=f"Total Cost (tax-included): {locale.currency(self.order[1])}", font=("Helvetica", 12, "bold"))
		totalCostLabel.grid(row=1, column=0)

		# Make labels for all order items and positoin them
		for x in range(len(self.orderItems)):
			# Get original product bought using the item's ID value, and the product through the "Items" table itself
			productID = self.orderItems[x][2]
			product = self.getItem(productID)
			# Make label for ordered item with product's name, the amount or quantity bought, and then the base price for that item
			orderItemLabel = ttk.Label(orderItemsSection, text=f"{product[1]} - Amount: {self.orderItems[x][3]} - Price: {locale.currency(product[2])}", font=("Helvetica", 10), anchor="center")
			orderItemLabel.grid(row=x, column=0, padx=10, pady=5)
		
		# BOOK MARK: Checking layout of the the receipt page, and also trying to import the db file functions instead of using the ones here		
		# Also have it take a boolean, on whether it's check out or just checking on an old purchase
		# Also check if points are working properly



	# Gets order from table
	def getOrder(self, orderID):
		self.master.cursor.execute(f"SELECT * FROM Orders WHERE id={orderID}")
		rows = self.master.cursor.fetchone()
		return rows

	# Get the purchased items and their quantities related to that order from the table
	def getOrderItems(self, orderID):
		self.master.cursor.execute(f"SELECT * FROM OrderBreakdown WHERE order_id={orderID}")
		rows = self.master.cursor.fetchall()
		return rows

	# Get item that they were buying from the Item table
	def getItem(self, itemID):
		self.master.cursor.execute(f"SELECT * FROM Items WHERE id={itemID}")
		rows = self.master.cursor.fetchone()
		return rows
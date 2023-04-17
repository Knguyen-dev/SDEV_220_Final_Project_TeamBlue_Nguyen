# Class that represents the shopping cart that each should just have one shopping cart

class ShoppingCart:
	def __init__(self, USER_ID):
		# Represents the user ID (ID in User table) that the shopping cart is associated with.
		# Simple Implementation: userID acts as an identifier to remind us who's linked to the cart; in this way the cart's contents aren't saved between sessions since we aren't storing them, but it's a lot more simple which is good enough.
		# In this case, we likely just need a "User" database table, and we just need a user to be added to the database so that we can use its database ID to pass to ShoppingCart. 


		self._USER_ID =  USER_ID
		# Will be a dictionary, with keys being the database ID values of the items in the cart, and values being the quantity of those items. 
		self._cartItems = dict()
		self._totalCost = 0
	
	# Function to add or update items in the cart
	# If when we add new items it creates a new pair, but if the key is already existing we update the quantity of old items in the cart; NOTE: itemQuantity shouldn't be 0 or negative
	def updateCartItem(self, itemID, itemQuantity):
		self._cartItems[itemID] = itemQuantity

	# Function to completely remove items from the cart; deleting their key; NOTE: user shouldn't be able to remove an item that isn't in the cart in the first place
	def removeCartItem(self, itemID):
		del self._cartItems[itemID]

	# Returns the items of the shopping cart as a list of tuples in form (itemID from item table, quantity of that item)
	def getCartItems(self):
		itemList = []
		for itemData in self._cartItems.items():
			itemList.append(itemData)
		return itemList

	# Calculates the current cost of all of the items in the cart and updates totalCost attribute, and returns it 
	def getTotalCost(self):
		"""
		Idea:

		self._totalCost = 0 # Set the totalCost to 0, then sum all prices 
		for each ID in our shopping cart:
			itemPrice = price of item that was queried from "items" database by id
			orderCost = itemPrice * quantity of that specific item;
			self._totalCost += orderCost  
		return self._totalCost; 
		"""
		pass
	
	# Returns the userID of the "User" associated with the shopping cart
	def getUserID(self):
		return self._USER_ID

	# Returns the below string when trying to print the function
	def __repr__(self):
		self.getTotalCost() # update the total cost of the shopping cart 
		return f"Cart UserID: {self._USER_ID}\nItems in Cart: {self.getCartItems()}\nTotal Cart Cost: {self._totalCost}"
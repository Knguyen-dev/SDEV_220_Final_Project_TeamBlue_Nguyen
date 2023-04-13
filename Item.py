# Class that represents an Item. Items are first added to database, and then queried. With the queried information we make it into a class. 

class Item:
	def __init__(self, itemName, itemPrice, itemImage, itemDesc):
		self._itemName = itemName
		self._itemPrice = itemPrice 
		self._itemImage = itemImage # represents the source or path of the image
		self._itemDesc = itemDesc # represents the description of the item
	
	# Setter functions: Methods themselves just change the instance attributes, so we can change attributes with methods, then we can eventually pass our new updated instance into a function that updates that 
	# item in the "Items" database table. We just query by itemID, and then pass the new item instance to update its information in the database with our new data.
	# NOTE: Possible that we may only use setters when modifying the items database
	def setItemName(self, newName):
		self._itemName = newName
	def setItemPrice(self, newPrice):
		self._itemPrice = newPrice
	def setItemImage(self, newImage):
		self._itemImage = newImage
	def setItemDescription(self, newDesc):
		self.itemDesc = newDesc

	# Here are our getters for the Item class
	def getItemName(self):
		return self._itemName
	def getItemPrice(self):
		return self._itemPrice
	def getItemImage(self):
		return self._itemImage
	def getItemDescription(self):
		return self._itemDesc

	# For printing an item class instance
	def __repr__(self):
		return f"Item: {self._itemName}\nPrice: {self._itemPrice}\nImage Location: {self._itemImage}\nDescription: {self._itemDesc}"
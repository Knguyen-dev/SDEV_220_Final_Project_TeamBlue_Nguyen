# Class purchase: Representing an order or purchase that a user makes. Think of it as a receipt that holds the id of the order and other basic information about the order
# Requirements: A "Purchases" table that has id (primary key), user_Id (foreign key, representing user who made the purchase), totalCost (total cost of the purchase), totalQuantity (representing total quantity of things purchased), and 
# the time of purchase (column type "TIMESTAMP" in sqlite I think).

# Procedure: It should just be after they checkout, we create the class, use the information from the class to put it in the database. Then I think we store the class into recentPurchases array. This is so that we can display
# the user's recent purchases, like show the total cost and total items bought. If needed we can go a step further and give them an average total cost of their recent, maybe last 3, purchases. 

import datetime


# timeValue = datetime.datetime.now(); gets the time and creates a datetime object
# strftime (string format time): takes a datetime object and turns it into a string, then you can put it into a database;
# strptime turns string into a datetime object; you'd retrieve the time as a string from the database and then convert it back into a datetime object so our Purchase class can handle it as an attribute

class Purchase:
	# Upper casing to indicate that they're constants
	def __init__(self, USER_ID, TOTAL_COST, TOTAL_QUANTITY, PURCHASE_DATE = None):
		self._USER_ID = USER_ID
		self._TOTAL_COST = TOTAL_COST 
		self._TOTAL_QUANTITY = TOTAL_QUANTITY
		
		# NOTE: There are two scenarios
		# 1. We are querying from database for an existing purchase with a time of purchase (in string form), then we call the constructor and put it back into datetime object form so our class can handle it. We aren't going to get involved
		# with the datetime object, we just know it stores the time so just abstract it, we are going to return and convert it that's all.
		# 2. We have a new purchase so we don't put in an argument for PURCHASE_DATE, which allows the class to be created with a datetime object with current date. Which we can later put into the database after returning its string form.

		if PURCHASE_DATE is  None:
			# Creates a datetime object with the current time since no time was provided; 
			self._PURCHASE_DATE = datetime.datetime.now()
		else:
			# PURCHASE_DATE (string) in form "2023-04-18 14:36:12" was provided, so we convert into a datetime object. 
			self._PURCHASE_DATE = datetime.datetime.strptime(PURCHASE_DATE, '%Y-%m-%d %H:%M:%S')

	# Get functions for Purchase 
	def getUserID(self):
		return self._USER_ID
	def getTotalCost(self):
		return self._TOTAL_COST
	def getTotalQuantity(self):
		return self._TOTAL_QUANTITY
	def getPurchaseDate(self):
		return self._PURCHASE_DATE.strftime('%Y-%m-%d %H:%M:%S')
	def __repr__(self):
		return f"User ID: {self._USER_ID}\nTotal Cost: {self._TOTAL_COST}\nTotal Item Quantity: {self._TOTAL_QUANTITY}\n{self.getPurchaseDate()}"
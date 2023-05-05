# Class purchase: Representing an order or purchase that a user makes. Think of it as a receipt that holds the id of the order and other basic information about the order
# Requirements: A "Purchases" table that has id (primary key), user_Id (foreign key, representing user who made the purchase), totalCost (total cost of the purchase), totalQuantity (representing total quantity of things purchased), and 
# the time of purchase (column type "TIMESTAMP" in sqlite I think).

# Procedure: It should just be after they checkout, we create the class, use the information from the class to put it in the database. Then I think we store the class into recentPurchases array. This is so that we can display
# the user's recent purchases, like show the total cost and total items bought. If needed we can go a step further and give them an average total cost of their recent, maybe last 3, purchases. 
import sqlite3


class Purchase:
	# Upper casing to indicate that they're constants; using default variables so that 
	# We can access a purchase constructor f
	def __init__(self, USER_ID, TOTAL_COST, TOTAL_QUANTITY):


		self._USER_ID = USER_ID
		self._TOTAL_COST = TOTAL_COST 
		self._TOTAL_QUANTITY = TOTAL_QUANTITY


		self.conn = sqlite3.connect("./assets/PyProject.db")
		self.cursor = self.conn.cursor()

		with self.conn:
			self.cursor.execute(f"INSERT INTO Orders (user_id, total_quantity, total) VALUES (:user_id, :total_quantity, :total)",
		       {
			       "user_id": self._USER_ID,
			       "total_quantity": self._TOTAL_QUANTITY,
			       "total": self._TOTAL_COST
			   })


	# Get functions for Purchase 
	def getUserID(self):
		return self._USER_ID
	def getTotalCost(self):
		return self._TOTAL_COST
	def getTotalQuantity(self):
		return self._TOTAL_QUANTITY
	def __repr__(self):
		return f"User ID: {self._USER_ID}\nTotal Cost: {self._TOTAL_COST}\nTotal Item Quantity: {self._TOTAL_QUANTITY}"
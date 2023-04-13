# NOTE: Just a draft, not set in stone; since we're using tkinter and databases our code is likely to change a lot if we tihnk about how things will work more


# Class representing what individual users or consumer accounts may look like 
class User:
	def __init__(self, username, firstName, lastName, shippingAddress, emailAddress):				
		# Initialize User attributes that the user will input in a form or something similar; "_" just indicates private attribute
		self._username = username 
		self._firstName = firstName 
		self._lastName = lastName
		self._shippingAddress = shippingAddress  
		self._emailAddress = emailAddress 
		
		# When we create accounts, the points and amount of money is going to be 0, accounts don't start off with money
		# As well as this recentPUrchases is empty
		self._userPoints = 0 
		self._userBalance = 0 
		self._recentPurchases = [] # list of integers that represent id for purchase table

		# NOTE: Add shopping cart attribute which is another class for one to one relationship
		# Represents the one shopping cart instance instance that they each User is linked to 

	# Setter functions to change attributes of User instances; obviously include functionality to save the new information to a database when finished.
	def setUsername(self, newUsername):
		self._username = newUsername
	def setFirstName(self, newFirstName): # later have functionality that only accepts alphabetic characters
		self._firstName = newFirstName
	def setLastName(self, newLastName):
		self._lastName = newLastName
	def setShippingAddress(self, newShippingAddress):
		self._shippingAddress = newShippingAddress
	def setEmailAddress(self, newEmailAddress): # it's easier to assume that they enter a valid email
		self._emailAddress = newEmailAddress

	# NOTE: userPoints or userBalance should never be below zero
	def setUserPoints(self, amount):
		self._userPoints = amount

	def setUserBalance(self, amount):
		self._userBalance = amount
	
	# Adds a purchase id to the front of the recentPurchases array 
	def addRecentPurchases(self, newPurchase):
		self._recentPurchases.insert(0, newPurchase) 
	# Here we simulate removing a purchase from the back of the array, maybe when there's more than a certain amount it removes the oldest one
	def removeRecentPurchases(self):
		self.recentPurchases.pop()

	# Getter functions to get user instance attributes
	def getUsername(self):
		return self._username
	def getFirstName(self):
		return self._firstName
	def getLastName(self):
		return self._lastName
	def getShippingAddress(self):
		return self._shippingAddress
	def getEmailAddress(self):
		return self._emailAddress
	def getPoints(self):
		return self._userPoints
	def getBalance(self):
		return self._userBalance
	def getRecentPurchases(self):
		return self._recentPurchases

	# Function prints "User" instances by showing this string 
	def __repr__(self):
		return f"Username: {self._username}\nFirst name: {self._firstName}\nLast name: {self._lastName}\nShipping Address: {self._shippingAddress}\nEmail Address: {self._emailAddress}\nBalance: {self._userBalance}\nPoints: {self._userPoints}"
		
		
def main():
	user1 = User("David42", "David", "Bills", "123 English CT", "DB82@gmail.com")
	
main()
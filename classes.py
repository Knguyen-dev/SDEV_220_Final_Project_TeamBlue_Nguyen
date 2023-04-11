# Here is where we create the classes for the system, and then we will be able to import these classes to other files
# Or maybe along the way we decide on a different organizational style when making the code


# Create class representing individual users or consumer accounts
class User:
		def __init__(self, username, firstName, lastName, shippingAddress, emailAddress):
				
				# The "_" to just indicate that it's a private variable (can't be accessed outside of class, must use methods to do so), 
				# this is just convention as python doesn't actually have private variables, so I'm just doing to indicate

				# Initialize User attributes that the user will input in a form or something similar
				self._username = username 
				self._firstName = firstName 
				self._lastName = lastName
				self.shippingAddress = shippingAddress  
				self._emailAddress = emailAddress 
				
				# When we create accounts, the points and amount of money is going to be 0, accounts don't start off with money
				# As well as this recentPUrchases is empty 
				self._userPoints = 0 
				self._userBalance = 0 
				self._recentPurchases = [] 

				# A good alternative to self.lastPurchase would be having an id of the last receipt or purchase that they checked out
				# self.lastPurchase = ""

				# Represents shopping cart class instance that they 
		
		# Setter functiosn to change attributes of User instance; obviously include functionality to save the new information to a database when finished.
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

		# For when the user is getting or using points on their account
		def addUserPoints(self, amount):
			self._userPoints += amount
		def subtractUserPoints(self, amount): # May need error handling to make sure userPoints doesn't go below zero
			self._userPoints  -= amount
		
		# For when the user is spending or adding money to their account
		def addUserBalance(self, amount):
			self._userBalance += amount
		def subtractUserBalance(self, amount):
			self._userBalance -= amount
		
		# I'm probably going to move forward, with it acting as receipts and purchase receipt id for purchase history
		# def setPurchaseHistory()
		# getPurchaseHistory()
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
		
def main():
	stuff = "Just the starting message in main"
	print(stuff)
main()
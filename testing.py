import sys
import os

from classes.User import User

myUser = User("knguyen44", "Kevin", "Nguyen", "123 ShippingHouse Drive", "knguyen44@ivytech.edu")

userAttributeNames = ["Username", "First Name", "Last Name", "Email", "Shipping Address", "Balance", "Points"]

for x in range(len(userAttributeNames)):
    print(myUser.getAttributeByName(userAttributeNames[x]))
# SDEV_220_Final_Project_TeamBlue
Team Blue Kroger Shopping App

+ How to run: 
1. Download this project, as a zip file or using your preferred method. 
2. Make sure the project director y's structure matches the one used on github.
3. Then in the base directory of your project run the "Main.py" file e.g. "python Main.py", and this starts the program

+ Files and folders
- Main.py: Main python file where the core of the application lives. Contains page navigation, navbar, and important master classes/variables that are used throughout the program.
- testing.py: Just a testing python file that's used to test sample code, not actually involved in the functionality of the project/application
- theme: Contains themes for the visual look of the website
- pages: Contains individual pages, represented as classes, that user navigates to throughout the website
	1. cartPage: Shopping cart page that lets users see what's in their shopping cart and to check out.
	2. homePage: The home page with the products, buy button, search, etc.
	3. productPage: Page that shows the extra information about the product
	4. receiptPage: Page that allows users to see receipt of their purchases
	5. userChangePassword: Page that allows users to change the password of their current acccount 
	6. userDelete: Page that allows users to delete their account, which is the account that's currently logged in  
	7. userEdit: Page for users to edit basic account information such as their name, address, etc.
	8. userLogin: Page for users to log into their accounts
	9. userManageBalance: Page for manipulating and changing wallet balance of current user 
	10. userPage: Page for showing the account information for the user that's currently logged into the application
	11. userRegister: Page for registering or creating a new user account
- classes: Contains only backend classes, for data structures representing users, shopping carts, etc.
	1. Item: For item class
	2. Purchase: Class for making purchases and adding them to the database
	3. ShoppingCart: Class for storing items
	4. User: User class for storing user information
	5. utilities: Module for some input handling

- assets: Contains python file for handling database manipulation, and database file with all of our data.
- images: Contains images used for the project
- .tcl files: Theme files


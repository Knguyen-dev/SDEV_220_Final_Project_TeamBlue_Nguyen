import importlib
import sys
import sqlite3

## Tkinter and Tkinter Framework
import tkinter as tk
from tkinter import Scrollbar, ttk
import ttkbootstrap as tkb
from ttkbootstrap.constants import *
from ttkbootstrap.style import Bootstyle
## Image imports
from PIL import Image, ImageTk
from urllib.request import urlopen

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Kroger")
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        self.geometry("%dx%d" % (width, height))
        self.conn = sqlite3.connect('assets/PyProject.db')
        self.cursor = self.conn.cursor()
        self.loggedinUser = None

        self.createNavbar()
        self.current_page = None      
        self.openPage("homePage")

    ## function: loadPage(page_name: str)
    ## This function is called to check if a class exists inside the pages directory
    ## if the page exists, it imports the page class and returns it to the caller.
    def loadPage(self, page_name):
        try:
            # import the module using the full path
            module = importlib.import_module(f"pages.{page_name}")
            # get the page class from the module
            page_class = getattr(module, page_name)
            return page_class
        except (ImportError, AttributeError):
            print(f"Error: Page {page_name} does not exist.")
            return None

    ## function: openPage(page_name: str, *args: any)
    ## This function is called to open a new page, It imports the page class using load_page,
    ## If the page exists it destroys the current and replaces with new page class
    def openPage(self, page_name, *args):
        page_class = self.loadPage(page_name)
        if page_class is None:
            return

        if self.current_page:
            self.current_page.destroy()

        self.current_page = page_class(self, self, *args)
        self.current_page.pack(fill='both', expand=True)

    ## function createNavbar()
    ## Creates the navbar and all respective buttons
    def createNavbar(self):
        # create the top menu
        self.navbar = tkb.Frame(self, bootstyle="primary")
        self.navbar.pack(fill=X, ipady=10, side=TOP)

        #logo frame
        self.logoFrame = tkb.Frame(self.navbar, bootstyle="primary")
        self.logoFrame.pack(fill=Y, side=LEFT)
        #logo
        self.logo = tkb.Button(self.logoFrame, width=10, text="Kroger", command=lambda: self.openPage("homePage"))
        self.logo.pack(side=LEFT, ipady=8, padx=2)

        # Search frame
        self.searchFrame = tkb.Frame(self.navbar, bootstyle="primary")
        self.searchFrame.pack(fill=Y, side=LEFT)
        # Search bar and button
        self.searchBar = tkb.Entry(self.searchFrame, width=180, bootstyle="secondary")
        self.searchBar.pack(side=LEFT, ipady=8, padx=2)
        self.searchButton = tkb.Button(master=self.searchFrame, text='Search', compound=RIGHT, command= lambda: self.searchFunction())
        self.searchButton.pack(fill=Y, side=RIGHT)

        # user frame
        self.userFrame = tkb.Frame(self.navbar, bootstyle="primary")
        self.userFrame.pack(fill=Y, side=RIGHT)
        # user / cart button
        self.cartButton  = ttk.Button(master=self.userFrame, text='Cart', compound=RIGHT, command=lambda: self.openPage("cartPage"))
        self.cartButton.pack(side=LEFT, ipadx=10, fill=Y)
        # user login button logic
        if self.loggedinUser is not None:
            self.userButton  = ttk.Button(master=self.userFrame, text='User', compound=RIGHT, command=lambda: self.openPage("userPage", self.loggedinUser))
            self.userButton.pack(side=LEFT, ipadx=10, fill=Y)
        else:
            self.userButton  = ttk.Button(master=self.userFrame, text='Login', compound=RIGHT, command=lambda: self.openPage("userLogin"))
            self.userButton.pack(side=LEFT, ipadx=10, fill=Y)
            


    ## function searchFunction()
    ## Grabs text from inside of searchBar Entry and sends data to homePage
    def searchFunction(self):
        searchItem = self.searchBar.get()
        self.openPage("homePage", searchItem)


if __name__ == "__main__":
    app = App()
    app.mainloop()

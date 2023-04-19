import tkinter as tk
from tkinter import Scrollbar, ttk
import ttkbootstrap as tkb
from ttkbootstrap.constants import *
from ttkbootstrap.style import Bootstyle


from PIL import Image, ImageTk
from urllib.request import urlopen
import io
import sqlite3

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Kroger")
        self.state("zoomed")

        self.conn = sqlite3.connect('assets/PyProject.db')
        self.cursor = self.conn.cursor()


        # create the top menu
        self.navbar = tkb.Frame(self, bootstyle="primary")
        self.navbar.pack(fill=X, ipady=10, side=TOP)

        self.logoFrame = tkb.Frame(self.navbar, bootstyle="primary")
        self.logoFrame.pack(fill=Y, side=LEFT)
        
        # Search bar
        self.logo = tkb.Label(self.logoFrame, width=10, text="Kroger", bootstyle="inverse-primary", font=("Helvetica", 14))
        self.logo.pack(side=LEFT, ipady=8, padx=2)

        self.searchFrame = tkb.Frame(self.navbar, bootstyle="primary")
        self.searchFrame.pack(fill=Y, side=LEFT)
        # Search bar
        self.searchBar = tkb.Entry(self.searchFrame, width=180, bootstyle="secondary")
        self.searchBar.pack(side=LEFT, ipady=8, padx=2)

        self.searchButton = tkb.Button(master=self.searchFrame, text='Search',
            compound=RIGHT
            )
        self.searchButton.pack(fill=Y, side=RIGHT)
        


        self.userFrame = tkb.Frame(self.navbar, bootstyle="primary")
        self.userFrame.pack(fill=Y, side=RIGHT)
        self.main_button  = ttk.Button(
            master=self.userFrame, text='Cart',
            compound=RIGHT
        )
        self.main_button.pack(side=LEFT, ipadx=5, ipady=5, fill=Y)
        self.settings  = ttk.Button(
            master=self.userFrame, text='User',
            compound=RIGHT

        )
        self.settings.pack(side=LEFT, ipadx=5, ipady=5, padx=(1, 0), fill=Y) 

        # create the content frame
        self.content = tk.Frame(self)
        self.content.place(relx=.5, rely=0.55, anchor="c")

        Scrollbar(self, orient='vertical')


        self.getProducts()

    def createProductDisplay(self, product):
        product_card = tkb.Frame(self.content, width=200, height=200,  bootstyle=PRIMARY)
        imageFrame = tkb.Frame(product_card, height=120, bootstyle=PRIMARY)

        response = urlopen(product[4])
        data = response.read()
        image = Image.open(io.BytesIO(data))
        image = image.resize((150, 150))
        image = ImageTk.PhotoImage(image=image)
        image_label = tkb.Label(imageFrame, image=image)
        image_label.image = image
        image_label.grid(row=0, column=0, sticky=tk.NSEW, padx=10, pady=10)
        imageFrame.pack(fill=X)

        detailFrame = tkb.Frame(product_card, height=80, bootstyle=PRIMARY)

        price_label = tkb.Label(detailFrame, text=product[2], font=("Helvetica", 10), width=40, anchor="w")
        price_label.grid(row=0, column=0, sticky=tk.NSEW)

        name_label = tkb.Label(detailFrame, text=product[1], font=("Helvetica", 10), width=40, anchor="w")
        name_label.grid(row=1, column=0, sticky=tk.NSEW)
        detailFrame.pack(fill=X)
        row = (len(self.content.winfo_children())-1) // 4
        col = (len(self.content.winfo_children())-1) % 4
        product_card.grid(row=row, column=col, padx=10, pady=10)
        product_card.grid_rowconfigure(0, weight=1)




    def searchProducts(self, *args):
        searchedProduct = self.searchVar.get()
        self.cursor.execute("SELECT * FROM items WHERE name LIKE ? LIMIT 6", ('%' + searchedProduct + '%',))
        rows = self.cursor.fetchall()

        for row in rows:
            self.createProductDisplay(row)

    def getProducts(self):
       self.cursor.execute("SELECT * FROM items LIMIT 12")
       rows = self.cursor.fetchall()
       for row in rows:
            self.createProductDisplay(row)

if __name__ == "__main__":
    app = App()
    app.mainloop()

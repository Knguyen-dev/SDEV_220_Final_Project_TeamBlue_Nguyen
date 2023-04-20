import tkinter as tk
from tkinter import Scrollbar, ttk
import ttkbootstrap as tkb
from ttkbootstrap.constants import *
from ttkbootstrap.style import Bootstyle
from PIL import Image, ImageTk
from urllib.request import urlopen
import io
import sqlite3

class cartPage(tk.Frame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.content = tkb.Frame(self)
        self.content.pack(fill=BOTH, expand=True)
        self.content.rowconfigure(0, weight=1) # set row 0 to expand vertically

        self.priceFrame = tkb.Frame(self.content, bootstyle=PRIMARY)
        self.priceFrame.pack(fill="y", ipadx=100, side=LEFT)
        self.priceTitle = tkb.Label(self.priceFrame, text="Summary", font=('Roboto', 18, 'bold'), bootstyle='inverse-primary')
        self.priceTitle.grid(row=0, column=0)

        self.itemsFrame = tk.Frame(self.content)
        self.itemsFrame.pack(fill=Y, ipadx=20, side=RIGHT)

        products = [
            ["Eggs", "https://m.media-amazon.com/images/I/41Yrtf5nzkL.jpg", "A carton of 12 eggs", "2.39"],
            ["Milk", "https://i5.walmartimages.com/asr/3592de4c-2d2d-4285-afbf-f0508775bd58_2.bb23225176016b4d5ce96c4efed80382.jpeg", "A gallon of milk", "2.99"]
        ]

        for product in products:
            self.createCartDisplay(product)

    def createCartDisplay(self, product):
        cartItem = tk.Frame(self.content, highlightbackground="#eee", highlightthickness=1)

        imageFrame = tkb.Frame(cartItem, height=120, width=120)
        response = urlopen(product[1])
        data = response.read()
        image = Image.open(io.BytesIO(data))
        image = image.resize((120, 120))
        image = ImageTk.PhotoImage(image=image)
        image_label = tkb.Label(imageFrame, image=image)
        image_label.image = image
        image_label.grid(row=0, column=0, sticky=tk.EW, padx=3, pady=3)
        imageFrame.grid(row=0, column=0, sticky=tk.NS, padx=3, pady=3)

        name_label = tkb.Label(cartItem, text=product[0], font=("Helvetica", 10, 'bold'), width=60, anchor="w")
        name_label.grid(row=0, column=1, sticky=tk.NSEW)

        description = tkb.Label(cartItem, text=product[2], font=("Helvetica", 10), width=60, anchor="w")
        description.grid(row=1, column=1, sticky=tk.NSEW)

        price = tkb.Label(cartItem, text=product[3], font=("Helvetica", 14, 'bold'), width=20, anchor="e")
        price.grid(row=0, column=2, sticky=tk.NSEW)

        cartItem.pack(fill=X, ipady=10, side=TOP)



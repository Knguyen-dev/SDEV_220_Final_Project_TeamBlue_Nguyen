from threading import Thread
import tkinter as tk
from tkinter import Scrollbar, ttk
import ttkbootstrap as tkb
from ttkbootstrap.constants import *
from ttkbootstrap.style import Bootstyle
from PIL import Image, ImageTk
from urllib.request import urlopen
import io
import sqlite3

class homePage(tk.Frame):
    def __init__(self, master, app, *args):
        super().__init__(master)
        self.master = master
        self.app = app
        self.homePage = tkb.Frame(self.app)
        self.homePage.place(relx=.5, rely=0.55, anchor="c")
        ## db
        self.conn = sqlite3.connect('assets/PyProject.db')
        self.cursor = self.conn.cursor()

        Scrollbar(self, orient='vertical')

        if args:
            self.searchProducts(args[0])
        else:
            self.getProducts()

        for i in range(3):
            self.homePage.grid_rowconfigure(i,  weight =1)
        for i in range(4):
            self.homePage.grid_columnconfigure(i,  weight =1)

    def createProductDisplay(self, product):
        product_card = tkb.Frame(self.homePage, width=200, height=200,  bootstyle=PRIMARY)
        imageFrame = tkb.Frame(product_card, height=120, bootstyle=PRIMARY)

        response = urlopen(product[4])
        data = response.read()
        image = Image.open(io.BytesIO(data))
        image = image.resize((120, 120))
        image = ImageTk.PhotoImage(image=image)
        image_label = tkb.Label(imageFrame, image=image)
        image_label.image = image
        image_label.grid(row=0, column=0, sticky=tk.EW, padx=10, pady=10)
        imageFrame.pack(fill=X)

        detailFrame = tkb.Frame(product_card, height=80)

        price_label = tkb.Label(detailFrame, text=f"$ {product[2]}", font=("Helvetica", 10), width=40, anchor="w")
        price_label.grid(row=1, column=0, sticky=tk.NSEW)

        buyButton = tkb.Button(detailFrame, text="Add to cart")
        buyButton.grid(row=1, column=1, sticky=tk.NS)

        name_label = tkb.Label(detailFrame, text=product[1], font=("Helvetica", 10, 'bold'), width=40, anchor="w")
        name_label.grid(row=0, column=0, sticky=tk.NSEW)

        name_label.bind("<Button-1>", lambda e:self.master.openPage("productPage", product[0]))

        detailFrame.pack(fill=X)

        row = (len(self.homePage.winfo_children())-1) // 4
        col = (len(self.homePage.winfo_children())-1) % 4
        product_card.grid(row=row, column=col, padx=10, pady=10)
        product_card.grid_rowconfigure(0, weight=1)

    def thread(self, row):
            t1=Thread(target=self.createProductDisplay(row))
            t1.start()

    def searchProducts(self, searchedProduct):
        self.clear_all()
        self.cursor.execute("SELECT * FROM items WHERE name LIKE ? LIMIT 6", ('%' + searchedProduct + '%',))
        rows = self.cursor.fetchall()
        for row in rows:
            self.thread(row)

    def getProducts(self):
       self.cursor.execute("SELECT * FROM items LIMIT 12")
       rows = self.cursor.fetchall()
       for row in rows:
            self.thread(row)
        
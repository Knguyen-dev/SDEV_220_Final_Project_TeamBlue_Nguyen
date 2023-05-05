import tkinter as tk
from tkinter import Image, ttk
from PIL import Image, ImageTk
import sqlite3
import locale



class receiptPage(tk.Frame):
    def __init__(self, master, app, orderID):
        super().__init__(master)
        self.app = app
        self.content = tk.Frame(self)
        self.content.pack(fill='both', expand=True)
        self.conn = sqlite3.connect('assets/PyProject.db')
        self.cursor = self.conn.cursor()
        self.order = self.getOrder(orderID)
        self.items = self.getOrderItems(orderID)
        locale.setlocale(locale.LC_ALL, '')

        self.OrderFrameLabel = ttk.Label(self.content, text="Your Order Has Been Placed", font=("Helvetica", 32, 'bold'), justify="center", anchor="center")
        self.OrderFrameLabel.pack(fill='both', anchor='center')


        self.receiptFrame = tk.Frame(self.content)

        self.subtotalLabel = ttk.Label(self.receiptFrame, text=f"Order ID: {self.order[0]}", font=("Helvetica", 15, 'bold'), anchor="e")
        self.subtotalLabel.grid(row=1, column=0)
    
    
        self.ReceiptHolder = tk.Frame(self.receiptFrame, border=1, highlightthickness=1, highlightbackground="#eee")

        for item in self.items:
            product = self.getItem(item[2])
            cartItem = tk.Frame(self.ReceiptHolder)

            name_label = ttk.Label(cartItem, text=product[1], font=("Helvetica", 10, 'bold'), anchor="w")
            name_label.grid(row=0, column=1, sticky="n")

            price = ttk.Label(cartItem, text=product[2], font=("Helvetica", 13, 'bold'), width=20, anchor="e")
            price.grid(row=0, column=3, sticky="e")

            cartItem.columnconfigure(2, weight=1)
            cartItem.columnconfigure(3, weight=1)

            cartItem.pack(fill='x', ipady=10, side='top')

        self.totalsFrame = tk.Frame(self.ReceiptHolder)
        price = tk.Label(self.totalsFrame, text=f'Total Items: {self.order[3]}', font=("Helvetica", 13, 'bold'), width=20, anchor="s")
        price.grid(row=1, column=1)
        price = tk.Label(self.totalsFrame, text=f'Total Cost: {locale.currency(self.order[1])}', font=("Helvetica", 13, 'bold'), width=20, anchor="s")
        price.grid(row=2, column=1)
        self.totalsFrame.pack(fill='y', side='bottom',ipady=10, pady=(20,5), anchor="center")

        self.ReceiptHolder.grid(row=2, column=0, pady=(80,0), ipadx=10, ipady=10)
    

        self.receiptFrame.pack(fill='y', expand=True, anchor="center")
        
    def getOrder(self, orderID):
       self.cursor.execute(f"SELECT * FROM Orders WHERE id={orderID}")
       rows = self.cursor.fetchone()
       return rows
    
    def getOrderItems(self, orderID):
       self.cursor.execute(f"SELECT * FROM OrderBreakdown WHERE order_id={orderID}")
       rows = self.cursor.fetchall()
       return rows
    
    def getItem(self, itemID):
       self.cursor.execute(f"SELECT * FROM Items WHERE id={itemID}")
       rows = self.cursor.fetchone()
       return rows
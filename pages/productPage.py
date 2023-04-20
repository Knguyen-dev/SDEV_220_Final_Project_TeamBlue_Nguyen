import tkinter as tk
from tkinter import Scrollbar, ttk
import ttkbootstrap as tkb
from ttkbootstrap.constants import *
from ttkbootstrap.style import Bootstyle
from PIL import Image, ImageTk
from urllib.request import urlopen
import io
import sqlite3

class productPage(tk.Frame):
    def __init__(self, master, app, productID):
        super().__init__(master)
        self.app = app
        self.content = tkb.Frame(self.app)
        self.content.place(relx=.5, rely=0.55, anchor="c")
        
        self.conn = sqlite3.connect('assets/PyProject.db')
        self.cursor = self.conn.cursor()

        self.productInfo = self.getProduct(productID)[0]
        self.cartLabel = tkb.Label(self.content, text=f"{self.productInfo[1]}: {self.productInfo[2]}")
        self.cartLabel.pack()


    def getProduct(self, id):
       self.cursor.execute(f"SELECT * FROM items WHERE id={id}")
       product = self.cursor.fetchall()
       return product
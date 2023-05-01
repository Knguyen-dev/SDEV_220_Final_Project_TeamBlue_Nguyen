import tkinter as tk
from tkinter import Scrollbar, ttk
from PIL import Image, ImageTk
import locale

class cartPage(tk.Canvas):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.content = ttk.Frame(self)
        self.content.pack(fill='both', expand=True)
        self.content.rowconfigure(0, weight=1) # set row 0 to expand vertically 
        locale.setlocale(locale.LC_ALL, '')
        self.priceFrame = ttk.Frame(self.content)
        self.priceFrame.pack(fill="y", ipadx=100, side='left')
        self.priceTitle = ttk.Label(self.priceFrame, text="Summary", font=('Roboto', 18, 'bold'))
        self.priceTitle.grid(row=0, column=0)

        self.itemsFrame = ttk.Frame(self.content)
        self.itemsFrame.pack(fill='y', ipadx=20, side='right')
        self.cart = self.master.CartClass.getCartItems()
        self.cartItem = dict(dict())

        self.create_window((0,0), window=self.content, anchor='nw')

        # Attach the scrollbar to the canvas
        treeXScroll = Scrollbar(self, orient=tk.VERTICAL)
        treeXScroll.configure(command=self.yview)
        self.configure(yscrollcommand=treeXScroll.set)

        for items in self.cart:
            self.createCartDisplay(items[0], items[1])

        treeXScroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.update_idletasks()
        self.configure(scrollregion=self.bbox("all"))

        # Add a binding between the scrollbar and the scrollable frame
        self.content.bind("<Configure>", lambda e: self.configure(scrollregion=self.bbox("all")))
        self.content.configure(width=300)


    def createCartDisplay(self, product, quantity):
        cartItem = ttk.Frame(self.content)

        imageFrame = ttk.Frame(cartItem, height=120, width=120)
        image = Image.open(product[4])
        image = image.resize((120, 120))
        image = ImageTk.PhotoImage(image=image)
        image_label = ttk.Label(imageFrame, image=image)
        image_label.image = image
        image_label.grid(row=0, column=0, sticky=tk.EW, padx=3, pady=3)
        imageFrame.grid(row=0, column=0, sticky=tk.NS, padx=3, pady=3)

        name_label = ttk.Label(cartItem, text=product[1], font=("Helvetica", 10, 'bold'), width=60, anchor="w")
        name_label.grid(row=0, column=1, sticky=tk.NSEW)

        description = ttk.Label(cartItem, text=product[3], font=("Helvetica", 10), width=60, anchor="w")
        description.grid(row=1, column=1, sticky=tk.NSEW)
        ## Joes quantity incrementer 

        quantityVar = tk.StringVar(value = quantity)
        priceVar = tk.StringVar(value = locale.currency(product[2] * quantity))
        incrementerFrame = ttk.Frame(cartItem)
        decrementButton = ttk.Button(incrementerFrame,  text=" - ", command= lambda: self.sub(product))
        decrementButton.grid(row=0, column=0)
        quanityText = ttk.Entry(incrementerFrame, textvariable=quantityVar)
        quanityText.grid(row=0, column=1)
        incrementButton = ttk.Button(incrementerFrame,  text=" + ", command= lambda: self.add(product))
        incrementButton.grid(row=0, column=2)

        incrementerFrame.grid()
        price = ttk.Label(cartItem, textvariable=priceVar, font=("Helvetica", 14, 'bold'), width=20, anchor="e")
        price.grid(row=0, column=2, sticky=tk.NSEW)

        self.cartItem.update({product[0] : {'quantity': quantityVar, 'price': priceVar}})

        """
            {productID  {quantity : IntVar(), price : StringVar()}}
        """

        cartItem.pack(fill='x', ipady=10, side='top')

    def add(self, product):
        # Get the productID and price from the product object
        productID = product[0]
        price = product[2]
        # Get the quantity from the inside dictionary of the cartItem using the productID key
        # The 'quantity' key is paired with an IntVar() value, so use .get() to get the value as an integer
        a=int(self.cartItem.get(productID)['quantity'].get())
        b=a+1
        # Do the same with price, but set the value
        self.cartItem.get(productID)['price'].set(locale.currency((b * price)))
        # Update the quantity after it is all done
        self.cartItem.get(productID)['quantity'].set(b)
        # Update Cart Class with new Quantity
        self.master.CartClass.updateCartItem(product, b)
        return
    def sub(self, product):
        productID = product[0]
        price = product[2]
        a=int(self.cartItem.get(productID).get('quantity').get())
        b=a-1
        self.cartItem.get(productID).get('price').set(locale.currency((b * price)))
        self.cartItem.get(productID).get('quantity').set(b)
        self.master.CartClass.updateCartItem(product, b)

        return
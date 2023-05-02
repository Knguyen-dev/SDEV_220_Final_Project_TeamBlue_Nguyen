import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from urllib.request import urlopen
import io
import locale


BLUE = "#0f52a2"
PINK = "#f5f5f5"

class cartPage(tk.Frame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.content = tk.Frame(self)
        self.content.pack(fill='both', expand=True)
        self.content.rowconfigure(0, weight=1) # set row 0 to expand vertically 
        locale.setlocale(locale.LC_ALL, '')

        self.subTotalVar = tk.IntVar(value = self.master.CartClass.getTotalCost())
        self.taxVar = tk.IntVar(value = self.subTotalVar.get() * 0.07)
        self.totalVar = tk.IntVar(value = locale.currency(self.subTotalVar.get() + self.taxVar.get()))

        self.orderFrame = tk.Canvas(self.content, width=500)

        self.OrderFrameLabel = ttk.Label(self.orderFrame, text="Order Summary", font=("Helvetica", 18, 'bold'))
        self.OrderFrameLabel.grid(row=1, column=0, sticky="nw")

        self.subtotalLabel = ttk.Label(self.orderFrame, text="Subtotal: ", font=("Helvetica", 14))
        self.subtotalLabel.grid(row=2, column=0, sticky="nw")

        self.subtotalNumber = ttk.Label(self.orderFrame, textvariable=self.subTotalVar, font=("Helvetica", 14))
        self.subtotalNumber.grid(row=2, column=1, sticky="w")

        self.taxLabel = ttk.Label(self.orderFrame, text="Tax: ", font=("Helvetica", 14))
        self.taxLabel.grid(row=3, column=0, sticky="w")

        self.taxNumber = ttk.Label(self.orderFrame, textvariable=self.taxVar, font=("Helvetica", 14))
        self.taxNumber.grid(row=3, column=1, sticky="w")

        self.totatLabel = ttk.Label(self.orderFrame, text="Total: ", font=("Helvetica", 14))
        self.totatLabel.grid(row=4, column=0, sticky="w")

        self.totalNumber = ttk.Label(self.orderFrame, textvariable=self.totalVar, font=("Helvetica", 14))
        self.totalNumber.grid(row=4, column=1, sticky="w")

        self.orderFrame.pack(fill='y', ipadx=100, pady=10, side='right')
        

        """
        self.orderFrame = tk.Canvas(self.content, width=500, height=900)
        self.background_image = tk.PhotoImage(file='images/orderBackground.png')
        self.orderFrame.create_image(375, 350, image=self.background_image)
        self.orderFrame.create_text(525, 120, text="Order Summary", fill="black", font=("Helvetica", 18, 'bold'), anchor='ne')
        self.orderFrame.create_text(525, 160, text="Order Number: ", fill="black", font=("Helvetica", 14), anchor='ne')
        self.orderFrame.create_text(525, 240, text="Subtotal: $", fill="black", font=("Helvetica", 14), anchor='ne')
        self.orderFrame.create_text(525, 300, text="Tax: $", fill="black", font=("Helvetica", 14), anchor='ne')
        self.orderFrame.create_text(525, 360, text="Total: $", fill="black", font=("Helvetica", 14), anchor='ne')
        self.orderFrame.pack(fill='y', ipadx=100, side='right')
        self.orderFrame.configure(bg='#f5f5f5')
        """

        self.canvas = tk.Canvas(self.content, width=350, height=700)
        self.character_img = tk.PhotoImage(file='images/bagMan.png')
        self.canvas.create_image(190,475, image=self.character_img)
        self.bubble_img = tk.PhotoImage(file='images/bubbleText.png')
        self.canvas.create_image(140,140, image=self.bubble_img)
        self.canvas.pack(fill='both', expand=True, side='left')

        cart_label = ttk.Label(self.content, text="Your Items", font=("Helvetica", 14, 'bold'), width=60)
        cart_label.pack(fill='x', ipady=40, side='top')

        self.cart = self.master.CartClass.getCartItems()
        self.cartItem = dict(dict())
        
        for items in self.cart:
            self.createCartDisplay(items[0], items[1])

    def createCartDisplay(self, product, quantity):
        # Create section for each item
        cartItem = tk.Frame(self.content, highlightbackground=PINK)

        imageFrame = tk.Frame(cartItem, height=120, width=120, background=PINK)
        image = Image.open(product[4])
        image = image.resize((120, 120))
        image = ImageTk.PhotoImage(image=image)
        image_label = ttk.Label(imageFrame, image=image)
        image_label.image = image
        image_label.grid(row=1, column=0, sticky=tk.EW, padx=3, pady=3)
        imageFrame.grid(row=1, column=0, sticky=tk.NS, padx=3, pady=3)

        name_label = ttk.Label(cartItem, text=product[1], font=("Helvetica", 10, 'bold'), width=60, anchor="w")
        name_label.grid(row=2, column=1, sticky=tk.NSEW)

        description = ttk.Label(cartItem, text=product[3], font=("Helvetica", 10), width=60, anchor="w")
        description.grid(row=2, column=1, sticky=tk.NSEW)


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


        price = ttk.Label(cartItem, textvariable=priceVar, font=("Helvetica", 14, 'bold'), width=20, anchor="w")
        price.grid(row=2, column=2, sticky=tk.NSEW)

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
        ## Update the cost of totalCost
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
    
    
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from urllib.request import urlopen
import io
import locale
from classes.Purchase import *

BLUE = "#0f52a2"
PINK = "#f5f5f5"
ACCENT = "#21409A"

class cartPage(tk.Frame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.content = tk.Frame(self)
        self.content.pack(fill='both', expand=True)
        self.content.rowconfigure(0, weight=1) # set row 0 to expand vertically 
        locale.setlocale(locale.LC_ALL, '')
        
        self.subTotalVar = tk.DoubleVar(value=round((self.master.CartClass.getTotalCost()), 2))
        self.taxVar = tk.DoubleVar(value=round((self.subTotalVar.get() * 0.07), 2))
        self.totalVar = tk.DoubleVar(value=locale.currency(self.subTotalVar.get() + self.taxVar.get()))


        self.orderFrame = tk.Frame(self.content, width=700)

        self.OrderFrameLabel = ttk.Label(self.orderFrame, text="Order Summary", font=("Helvetica", 18, 'bold'), anchor="e")
        self.OrderFrameLabel.grid(row=0, column=0, columnspan=2)

        self.subtotalLabel = ttk.Label(self.orderFrame, text="Subtotal: ", font=("Helvetica", 14), anchor="e")
        self.subtotalLabel.grid(row=1, column=0)

        self.subtotalNumber = ttk.Label(self.orderFrame, textvariable=self.subTotalVar, font=("Helvetica", 14), anchor="e")
        self.subtotalNumber.grid(row=1, column=1)

        self.taxLabel = ttk.Label(self.orderFrame, text="Tax: ", font=("Helvetica", 14), anchor="e")
        self.taxLabel.grid(row=2, column=0)

        self.taxNumber = ttk.Label(self.orderFrame, textvariable=self.taxVar, font=("Helvetica", 14), anchor="e")
        self.taxNumber.grid(row=2, column=1)

        self.totalLabel = ttk.Label(self.orderFrame, text="Total: ", font=("Helvetica", 14), anchor="e")
        self.totalLabel.grid(row=3, column=0)

        self.totalNumber = ttk.Label(self.orderFrame, textvariable=self.totalVar, font=("Helvetica", 14), anchor="e")
        self.totalNumber.grid(row=3, column=1)


        self.buyButton = ttk.Button(self.orderFrame, text="Check out", style="TTButton", command=lambda : self.purchaseItems())
        self.buyButton.grid(row=4, column=0, columnspan=2, pady=15)

        self.orderFrame.pack(fill='y', padx=(100, 0), pady=10, ipadx=50, side='right', expand=False)
        

        self.canvas = tk.Canvas(self.content, width=250, height=700)
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
        cartItem = tk.Frame(self.content)

        imageFrame = tk.Frame(cartItem, height=80, width=80)
        image = Image.open(product[4])
        image = image.resize((120, 120))
        image = ImageTk.PhotoImage(image=image)
        image_label = ttk.Label(imageFrame, image=image)
        image_label.image = image
        image_label.grid(row=0, column=0, padx=3, pady=3)
        imageFrame.grid(row=0, column=0, sticky="ne", padx=3, pady=3, rowspan=2)


        name_label = ttk.Label(cartItem, text=product[1], font=("Helvetica", 10, 'bold'), anchor="w")
        name_label.grid(row=0, column=1, sticky="n")

        description = ttk.Label(cartItem, text=product[3], font=("Helvetica", 10), anchor="nw")
        description.grid(row=1, column=1, sticky="nw")


        quantityVar = tk.StringVar(value = quantity)
        priceVar = tk.StringVar(value = locale.currency(product[2] * quantity))
        incrementerFrame = ttk.Frame(cartItem)
        decrementButton = ttk.Button(incrementerFrame,  text=" - ", command= lambda: self.sub(product), width=5)
        decrementButton.grid(row=0, column=0)
        quanityText = ttk.Entry(incrementerFrame, textvariable=quantityVar, width=8)
        quanityText.grid(row=0, column=1)
        incrementButton = ttk.Button(incrementerFrame,  text=" + ", command= lambda: self.add(product), width=5)
        incrementButton.grid(row=0, column=2)
        incrementerFrame.grid(row=1, column=3, sticky="e")

        price = ttk.Label(cartItem, textvariable=priceVar, font=("Helvetica", 14, 'bold'), width=20, anchor="e")
        price.grid(row=0, column=3, sticky="e")

        cartItem.columnconfigure(2, weight=1)
        cartItem.columnconfigure(3, weight=1)

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
        self.updateSummary()

        return
    
    def sub(self, product):
        productID = product[0]
        price = product[2]
        a=int(self.cartItem.get(productID).get('quantity').get())
        b=a-1
        self.cartItem.get(productID).get('price').set(locale.currency((b * price)))
        self.cartItem.get(productID).get('quantity').set(b)
        self.master.CartClass.updateCartItem(product, b)

        self.updateSummary()

        return
    
    
    def updateSummary(self):
        self.subTotalVar.set(round(self.master.CartClass.getTotalCost(), 2))
        self.taxVar.set(round((self.subTotalVar.get() * 0.07), 2))
        self.totalVar.set(locale.currency(round((self.subTotalVar.get() + self.taxVar.get()), 2)))
        pass

    
    def purchaseItems(self):
        total = int(self.subTotalVar.get() + (self.subTotalVar.get() * 0.07))
        balance = int(self.master.loggedinUser.getBalance())

        # Gets cart items and sums up the total quantity of items
        cartItems = self.master.CartClass.getCartItems()
        totalQuantity = 0

        for item in cartItems:
            totalQuantity += item[1]
        
        # If they have enough money and it's a successful purchase
        if (balance - total) >= 0:
            # Changes user's balance and points; the point system is having 5% of the total be the amount of points they earn
            # Then save their new balance and points in the database, because I don't it has been done yet
            self.master.loggedinUser.setUserBalance((balance - total))
            currentPoints = self.master.loggedinUser.getPoints()
            earnedPoints = int(total * 0.05)
            self.master.loggedinUser.setUserPoints(currentPoints + earnedPoints)



            # Makes purchase and puts it into database
            Purchase(self.master.loggedinUser.getID(), total, totalQuantity)

            with self.master.conn:

                # Update the loggedinUser's balance and points in the database 
                self.master.cursor.execute(f'''UPDATE Users SET balance=:balance, points=:points WHERE id=:id''', 
                {
                    "balance": self.master.loggedinUser.getBalance(),
                    "points": self.master.loggedinUser.getPoints(),
                    "id": self.master.loggedinUser.getID()
                })



                # Gets the most recent purcahse from the databaseand gets the id
                self.master.cursor.execute("SELECT id FROM Orders ORDER BY id DESC LIMIT 1")
                purchaseID = self.master.cursor.fetchone()

                # For each cart item, insert it into OrderBreakdown with corresponding information
                for item in cartItems:
                    self.master.cursor.execute("INSERT INTO OrderBreakdown (order_id, item_id, quantity) VALUES (:order_id, :item_id, :quantity)", 
                    {
                        "order_id": purchaseID[0],
                        "item_id": item[0][0],
                        "quantity": item[1]
                    }                           
                    )

            # Calls function that empties the shopping cart, since they're done with the purchase
            self.master.CartClass.emptyShoppingCart()
            self.master.openPage("receiptPage", purchaseID[0])

            # Probably want them to be taken to another page after they're done with that
            # If not the receipt page, then we could probably take them back to the home page

            
        else:
            print("fail")
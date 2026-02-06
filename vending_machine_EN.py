import customtkinter as ctk
from tkinter import messagebox as mb
import random

# List of product names and their prices
products_name = ['Coke', 'Energy drink', 'Soda', 'Water', 'Sparkling water', 'Fruit juice']
products_price = [14.09, 9.49, 6.87, 7.99, 6.99, 7.79]

# Dictionary to store product information: name, price, quantity in cart, and stock
products = {}
for i in range(len(products_name)):
    products[f'Product_{i+1}'] = {
        'name': products_name[i],
        'price': products_price[i],
        'in_cart': 0,  # Quantity of the product in the cart
        'stock': random.randint(5, 10)  # Random initial stock between 5 and 10
    }

def only_number(char):
    """
    Validates if the input character is a number or a comma (for decimal values).
    Args:
        char (str): The character to validate.
    Returns:
        bool: True if the character is valid, False otherwise.
    """
    if char == '':
        return True
    if char.count(',') > 1:  # Only one comma allowed (for decimal values)
        return False
    if all(c in '0123456789,' for c in char):  # Check if all characters are numbers or commas
        return True
    return False

def change_exit(bill_value, amount):
    """
    Formats the change output message for bills and coins.
    Args:
        bill_value (str): The type of bill or coin (e.g., "one-hundred-dollar").
        amount (int): The quantity of bills or coins.
    Returns:
        str: Formatted message for the change.
    """
    output = ''
    if not 'cent' in bill_value and amount == 1:
        output += f'-> {amount} {bill_value} bill\n'
    elif 'cent' in bill_value and amount == 1:
        output += f'-> {amount} {bill_value} coin\n'
    elif 'cent' in bill_value and amount > 1:
        output += f'-> {amount} {bill_value} coins\n'
    elif amount == 0:
        return ''
    else:
        output += f'-> {amount} {bill_value} bills\n'
    return output

def bill_count(full_change, bill_value):
    """
    Counts how many bills or coins of a specific value fit into the remaining change.
    Args:
        full_change (float): The remaining change to be given.
        bill_value (float): The value of the bill or coin.
    Returns:
        int: The number of bills or coins of the specified value.
    """
    bill_amount = 0
    while full_change != 0:
        if full_change >= bill_value:
            full_change = round(full_change, 2) - bill_value
            bill_amount += 1
        else:
            break
    return bill_amount

def change_count(true_change, bill_amount, bill_value):
    """
    Updates the remaining change after subtracting the value of the bills or coins.
    Args:
        true_change (float): The remaining change.
        bill_amount (int): The number of bills or coins.
        bill_value (float): The value of the bill or coin.
    Returns:
        float: The updated remaining change.
    """
    true_change = true_change - (bill_amount * bill_value)
    return true_change

def products_in_cart(num, symbol):
    """
    Updates the quantity of a product in the cart and its stock.
    Args:
        num (int): The product number.
        symbol (str): '+' to add to cart, '-' to remove from cart.
    """
    if symbol == '-':
        products[f'Product_{num}']['in_cart'] -= 1
        products[f'Product_{num}']['stock'] += 1
        buttons[num-1].configure(text=f'{products[f"Product_{num}"]["name"]}\n$ {str(products[f"Product_{num}"]["price"]).replace(".",",")}\nstock: {products[f"Product_{num}"]["stock"]}')
        buttons[num-1].configure(state='normal')  # Re-enable the button if the product was removed from the cart
    else:
        if products[f'Product_{num}']['stock'] == 0:
            pass  # Do nothing if the product is out of stock
        else:
            products[f'Product_{num}']['in_cart'] += 1
            products[f'Product_{num}']['stock'] -= 1
            buttons[num-1].configure(text=f'{products[f"Product_{num}"]["name"]}\n$ {str(products[f"Product_{num}"]["price"]).replace(".",",")}\nstock: {products[f"Product_{num}"]["stock"]}')

    # Calculate the total value of the cart
    values = []
    for i in range(len(products)):
        values.append(products[f'Product_{i+1}']['price'] * products[f'Product_{i+1}']['in_cart'])
    total.configure(text=f'Total: $ {str(round(float(sum(values)), 2)).replace(".", ",")}')

    # Update the cart display
    if products[f'Product_{num}']['in_cart'] == 0:
        text_amount[num-1].grid_forget()
        minus_button[num-1].grid_forget()
    elif products[f'Product_{num}']['stock'] == 0:
        text_amount[num-1].configure(text=f'{products[f"Product_{num}"]["in_cart"]} {products[f"Product_{num}"]["name"]}')
        mb.showwarning('Out of stock', f'We have run out of {products[f"Product_{num}"]["name"]}')
        buttons[num-1].configure(state='disabled')  # Disable the button if the product is out of stock
    else:
        text_amount[num-1].configure(text=f'{products[f"Product_{num}"]["in_cart"]} {products[f"Product_{num}"]["name"]}')
        text_amount[num-1].grid(row=num-1, column=0, pady=2)
        minus_button[num-1].grid(row=num-1, column=1, padx=10)

def vending_machine():
    """
    Processes the purchase: calculates the total, checks the payment, and gives change if necessary.
    """
    try:
        values = []
        for i in range(len(products)):
            values.append(products[f'Product_{i+1}']['price'] * products[f'Product_{i+1}']['in_cart'])

        if entry.get() == '':
            mb.showwarning('No amount entered', 'Please enter an amount')
        else:
            amount_paid = float(entry.get().replace(',', '.'))
            amount_to_pay = float(sum(values))

            if amount_to_pay == 0.00:
                mb.showwarning('Empty cart', 'Your cart is empty')
            else:
                if amount_paid > amount_to_pay:
                    change = float(amount_paid) - amount_to_pay
                    output = f'Change to be received: ${change:.2f}\n'

                    # Calculate the number of each bill and coin for the change
                    bill_100 = bill_count(change, 100)
                    change = change_count(change, bill_100, 100)

                    bill_50 = bill_count(change, 50)
                    change = change_count(change, bill_50, 50)

                    bill_20 = bill_count(change, 20)
                    change = change_count(change, bill_20, 20)

                    bill_10 = bill_count(change, 10)
                    change = change_count(change, bill_10, 10)

                    bill_5 = bill_count(change, 5)
                    change = change_count(change, bill_5, 5)

                    bill_2 = bill_count(change, 2)
                    change = change_count(change, bill_2, 2)

                    bill_1 = bill_count(change, 1)
                    change = change_count(change, bill_1, 1)

                    coin_50 = bill_count(change, 0.50)
                    change = change_count(change, coin_50, 0.50)

                    coin_25 = bill_count(change, 0.25)
                    change = change_count(change, coin_25, 0.25)

                    coin_10 = bill_count(change, 0.10)
                    change = change_count(change, coin_10, 0.10)

                    coin_5 = bill_count(change, 0.05)
                    change = change_count(change, coin_5, 0.05)

                    coin_1 = bill_count(change, 0.01)
                    change = change_count(change, coin_1, 0.01)

                    # Format the change output message
                    output += '\nChange made up of:\n'
                    output += change_exit('$100 bill', bill_100)
                    output += change_exit('$50 bill', bill_50)
                    output += change_exit('$20 bill', bill_20)
                    output += change_exit('$10 bill', bill_10)
                    output += change_exit('$5 bill', bill_5)
                    output += change_exit('$2 bill', bill_2)
                    output += change_exit('$1 bill', bill_1)
                    output += change_exit('50-cent coin', coin_50)
                    output += change_exit('25-cent coin', coin_25)
                    output += change_exit('10-cent coin', coin_10)
                    output += change_exit('5-cent coin', coin_5)
                    output += change_exit('1-cent coin', coin_1)
                    mb.showinfo('Your change', output)

                    # Reset the cart and entry field
                    total.configure(text='Total: $ 0.00')
                    entry.delete(0, ctk.END)
                    for i in range(6):
                        products[f'Product_{i+1}']['in_cart'] = 0
                        text_amount[i].grid_forget()
                        minus_button[i].grid_forget()
                        if products[f'Product_{i+1}']['stock'] == 0:
                            products[f'Product_{i+1}']['stock'] = random.randint(5, 10)  # Restock the product
                            buttons[i].configure(text=f'{products[f"Product_{i+1}"]["name"]}\n$ {str(products[f"Product_{i+1}"]["price"]).replace(".", ",")}\nstock: {products[f"Product_{i+1}"]["stock"]}', state='normal')

                elif amount_paid < amount_to_pay and round(amount_to_pay - amount_paid, 2) == 1:
                    mb.showwarning('Insufficient money', f'Still missing: ${amount_to_pay - amount_paid:.2f} dollar')
                elif amount_paid < amount_to_pay and round(amount_to_pay - amount_paid, 2) > 1:
                    mb.showwarning('Insufficient money', f'Still missing: ${amount_to_pay - amount_paid:.2f} dollars')
                elif amount_paid < amount_to_pay and round(amount_to_pay - amount_paid, 2) < 1 and round(amount_to_pay - amount_paid, 2) > 0:
                    mb.showwarning('Insufficient money', f'Still missing: ${amount_to_pay - amount_paid:.2f} cents')
                else:
                    mb.showinfo('Exact money', 'No change needed')
    except ValueError:
        mb.showerror('Input error', 'Input error\nInvalid value. Use only numbers and commas')

# Create the main window
window = ctk.CTk()
ctk.set_appearance_mode("dark")
window.geometry('360x660')
vcmd = (window.register(only_number), '%P')
window.title('Vending Machine')

# Title label
ctk.CTkLabel(window, text='--- Vending Machine ---', font=('arial', 22, 'bold')).pack(pady=10)

# Entry frame for the amount of money
frame = ctk.CTkFrame(window)
frame.pack()
ctk.CTkLabel(frame, text='$', font=('arial', 16, 'bold')).pack(side=ctk.LEFT)
entry = ctk.CTkEntry(frame, width=80, validate='key', validatecommand=vcmd, font=('arial', 16, 'bold'))
entry.pack(side=ctk.LEFT, pady=5, padx=5)
entry.focus()

# Frame for the cart display
canva = ctk.CTkFrame(window, width=100, height=30)
canva.pack(pady=15)
ctk.CTkLabel(window, text='Choose one or more products:', font=('arial', 18, 'bold')).pack(pady=10)

# Lists to store cart labels and minus buttons
text_amount = [None] * 6
minus_button = [None] * 6
for i in range(len(text_amount)):
    text_amount[i] = ctk.CTkLabel(canva, text='', justify='left', font=('arial', 16, 'bold'))
    minus_button[i] = ctk.CTkButton(canva, width=30, text='-1', command=lambda i=i: products_in_cart(i+1, '-'), font=('arial', 12, 'bold'))

# Frame for product buttons
line = ctk.CTkFrame(window)
line.pack(pady=5)
buttons = [None] * 6
for i in range(len(buttons)):
    buttons[i] = ctk.CTkButton(
        line,
        font=('arial', 16),
        text=f'{products[f"Product_{i+1}"]["name"]}\n$ {str(products[f"Product_{i+1}"]["price"]).replace(".", ",")}\nstock: {products[f"Product_{i+1}"]["stock"]}',
        command=lambda i=i: products_in_cart(i+1, '+'),
        width=150
    )
    buttons[i].grid(pady=5, padx=5)
    if i < 2:
        buttons[i].grid(row=0)
    elif i < 4:
        buttons[i].grid(row=1)
    else:
        buttons[i].grid(row=2)
    if i % 2 == 1:
        buttons[i].grid(column=1)
    elif i % 2 == 0:
        buttons[i].grid(column=0)

# Label to display the total value of the cart
total = ctk.CTkLabel(window, text='Total: $ 0.00', font=('arial', 22, 'bold'))
total.pack()

# Button to finalize the purchase
final = ctk.CTkButton(window, text='FINALIZE PURCHASE', anchor='center', command=vending_machine, width=350, height=50, font=('arial', 20, 'bold'))
final.pack()

window.mainloop()

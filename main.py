# Copyright 2025 Parker Sherman
import requests
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from io import BytesIO

# This function get the country data from the API using the "requests" library
def fetch_country_data():
    country = country_entry.get().strip()
    if not country:
        messagebox.showwarning("Input Error", "Please enter a valid country")
        return
    
    url = f"https://restcountries.com/v3.1/name/{country}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()[0]
            display_country_data(data)
        else:
            messagebox.showerror("Error", f"Country '{country}' not found.")
            clear_display()
    except Exception as e:
        messagebox.showerror("Error", str(e))
        clear_display()

# Formats all the data from the country to be displayed
def display_country_data(data):
    name = data['name']['common']
    capital = ', '.join(data.get('capital', ['N/A']))
    region = data.get('region', 'N/A')
    population = f"{data.get('population', 0):,}"
    languages = ', '.join(data.get('languages', {}).values())
    currencies = ', '.join([f"{v['name']} ({v['symbol']})" for v in data.get('currencies', {}).values()])
    flag_url = data.get('flags', {}).get('png', 'N/A')

    result_text.set(f"""
    Country: {name}
    Capital: {capital}
    Region: {region}
    Population: {population}
    Languages: {languages}
    Currencies: {currencies}
    """.strip())

    # Code to Load the Countryls flag
    try:
        img_data = requests.get(flag_url).content
        img = Image.open(BytesIO(img_data)).resize((120, 80))
        tk_image = ImageTk.PhotoImage(img)
        flag_label.config(image=tk_image)
        flag_label.image = tk_image
    except Exception:
        flag_label.config(image='', text='[Flag not available]')

# clears the display of any output
def clear_display():
    result_text.set("")
    flag_label.config(image="")

# Simple GUI using tkinter
root = tk.Tk()
root.title("Country Finder")
root.geometry("500x400")
root.resizable(False, False)

style = ttk.Style()
style.configure("TButton", font=("Segoe UI", 10))
style.configure("TLabel", font=("Segoe UI", 10))

# Search Bar
frame = ttk.Frame(root, padding=10)
frame.pack(pady=10)

# Search bar for the user to enter the country
ttk.Label(frame, text="Enter Country Name:").grid(row=0, column=0, padx=5)
country_entry = ttk.Entry(frame, width=30)
country_entry.grid(row=0, column=1, padx=5)

# Button to fulfill the search request
search_button = ttk.Button(frame, text="Search", command=fetch_country_data)
search_button.grid(row=0, column=2, padx=5)

# For Output Display
result_text = tk.StringVar()
result_label = ttk.Label(root, textvariable=result_text, padding = 10, justify="left", wraplength=480)
result_label.pack(pady=10)

# Flag Image
flag_label = ttk.Label(root)
flag_label.pack()

# This button clears the output
clear_button = ttk.Button(root, text="Clear", command=clear_display)
clear_button.place(relx=0.99, rely=0.99, anchor="se")



# GUI Loop
root.mainloop()
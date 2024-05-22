# Property Tax Assessment and Payment Tracking Application
# This application is designed to help users manage their property tax assessments and payments.
# BY IAN CRIS P. VILLAVICENCIO AND MARC C. SIBUG -BS CPE 1A

import tkinter as tk
from tkinter import ttk
import sqlite3

conn = sqlite3.connect('property_tax.db')
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS property_tax (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    property_address TEXT,
    assessment_amount REAL,
    payment_amount REAL,
    payment_date TEXT
)""")

def add_property():
    """
    Add a new property to the database.
    """
    address = address_entry.get("1.0", "end-1c")
    try:
        assessment = float(assessment_entry.get("1.0", "end-1c"))
    except ValueError:
        assessment = 0.0
    try:
        payment = float(payment_entry.get("1.0", "end-1c"))
    except ValueError:
        payment = 0.0
    date = date_entry.get("1.0", "end-1c")

    c.execute("INSERT INTO property_tax (property_address, assessment_amount, payment_amount, payment_date) VALUES (?, ?, ?, ?)", (address, assessment, payment, date))
    conn.commit()
    refresh_table()
    clear_entries()

def edit_property():
    """
    Edit an existing property in the database.
    """
    selected = property_table.selection()
    if selected:
        id = property_table.item(selected)['values'][0]
        address = address_entry.get("1.0", "end-1c")
        try:
            assessment = float(assessment_entry.get("1.0", "end-1c"))
        except ValueError:
            assessment = 0.0
        try:
            payment = float(payment_entry.get("1.0", "end-1c"))
        except ValueError:
            payment = 0.0
        date = date_entry.get("1.0", "end-1c")

        c.execute("UPDATE property_tax SET property_address = ?, assessment_amount = ?, payment_amount = ?, payment_date = ? WHERE id = ?", (address, assessment, payment, date, id))
        conn.commit()
        refresh_table()
        clear_entries()

def delete_property():
    """
    Delete a property from the database.
    """
    selected = property_table.selection()
    if selected:
        id = property_table.item(selected)['values'][0]
        c.execute("DELETE FROM property_tax WHERE id = ?", (id,))
        conn.commit()
        refresh_table()

def view_properties():
    """
    Display all properties in the database.
    """
    refresh_table()

def refresh_table():
    """
    Refresh the property table with data from the database.
    """
    c.execute("SELECT * FROM property_tax")
    data = c.fetchall()
    property_table.delete(*property_table.get_children())
    for row in data:
        property_table.insert("", "end", values=row)

def clear_entries():
    """
    Clear the entry fields.
    """
    address_entry.delete("1.0", "end")
    assessment_entry.delete("1.0", "end")
    payment_entry.delete("1.0", "end")
    date_entry.delete("1.0", "end")

root = tk.Tk()
root.title("Property Tax Assessment and Payment Tracking")
root.configure(bg="black")  # Set the background color of the main window to black

# Set the style for the Treeview widget
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", background="black", foreground="green", fieldbackground="black", font=("Courier", 12, "bold"))
style.configure("Treeview.Heading", background="black", foreground="green", font=("Courier", 12, "bold"))
style.map("Treeview", background=[("selected", "green"), ("alternate", "black")], foreground=[("selected", "black"), ("alternate", "green")])

address_label = tk.Label(root, text="Property Address:", bg="black", fg="green", font=("Courier", 12, "bold"))
address_entry = tk.Text(root, height=1, width=30, font=("Courier", 12, "bold"), bg="black", fg="green", insertbackground="green")

assessment_label = tk.Label(root, text="Assessment Amount:", bg="black", fg="green", font=("Courier", 12, "bold"))
assessment_entry = tk.Text(root, height=1, width=30, font=("Courier", 12, "bold"), bg="black", fg="green", insertbackground="green")

payment_label = tk.Label(root, text="Payment Amount:", bg="black", fg="green", font=("Courier", 12, "bold"))
payment_entry = tk.Text(root, height=1, width=30, font=("Courier", 12, "bold"), bg="black", fg="green", insertbackground="green")

date_label = tk.Label(root, text="Payment Date:", bg="black", fg="green", font=("Courier", 12, "bold"))
date_entry = tk.Text(root, height=1, width=30, font=("Courier", 12, "bold"), bg="black", fg="green", insertbackground="green")

add_button = tk.Button(root, text="Add", command=add_property, bg="black", fg="green", font=("Courier", 12, "bold"))
edit_button = tk.Button(root, text="Edit", command=edit_property, bg="black", fg="green", font=("Courier", 12, "bold"))
delete_button = tk.Button(root, text="Delete", command=delete_property, bg="black", fg="green", font=("Courier", 12, "bold"))
view_button = tk.Button(root, text="View", command=view_properties, bg="black", fg="green", font=("Courier", 12, "bold"))

property_table = ttk.Treeview(root, columns=("id", "address", "assessment", "payment", "date"), style="Custom.Treeview")
property_table.tag_configure("oddrow", background="black", foreground="green")  # Set the foreground color for odd rows to green
property_table.tag_configure("evenrow", background="black", foreground="green")  # Set the foreground color for even rows to green
property_table.heading("#0", text="")
property_table.heading("id", text="ID")
property_table.heading("address", text="Address")
property_table.heading("assessment", text="Assessment")
property_table.heading("payment", text="Payment")
property_table.heading("date", text="Date")

# Layout the GUI
address_label.grid(row=0, column=0, padx=10, pady=10)
address_entry.grid(row=0, column=1, padx=10, pady=10)

assessment_label.grid(row=1, column=0, padx=10, pady=10)
assessment_entry.grid(row=1, column=1, padx=10, pady=10)

payment_label.grid(row=2, column=0, padx=10, pady=10)
payment_entry.grid(row=2, column=1, padx=10, pady=10)

date_label.grid(row=3, column=0, padx=10, pady=10)
date_entry.grid(row=3, column=1, padx=10, pady=10)

add_button.grid(row=4, column=0, padx=10, pady=10)
edit_button.grid(row=4, column=1, padx=10, pady=10)
delete_button.grid(row=4, column=2, padx=10, pady=10)
view_button.grid(row=4, column=3, padx=10, pady=10)

property_table.grid(row=5, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
root.mainloop()
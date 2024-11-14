
'''
This user-friendly application is designed to help organizations efficiently manage member information, 
track national dues payments, and monitor attendance at events. 
The app allows members to register by entering  their personal details—such as first name, last name, 
D100 number, NSBE ID, and email;
which are securely stored in a centralized database.

'''
# Import the SQLite library to interact with the database
import sqlite3  

# Function to create the database and tables if they don't already exist
def create_database():
    conn = sqlite3.connect('NSBE.db')  # Connect to the database (creates if it doesn't exist)
    c = conn.cursor()  # Create a cursor object to interact with the database

    # Create 'members' table if it doesn't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            first_name TEXT,  
            last_name TEXT,  
            d100_number TEXT,  
            nsbe_id TEXT,  
            email TEXT,  
            dues_paid BOOLEAN,  
            attendance_count INTEGER  
        )
    ''')

    # Create 'events' table if it doesn't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            event_name TEXT, 
            event_date TEXT 
        )
    ''')

    # Create 'attendance' table to track member attendance at events
    c.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            member_id INTEGER,  
            event_id INTEGER,  
            attended BOOLEAN,  
            FOREIGN KEY(member_id) REFERENCES members(id), 
            FOREIGN KEY(event_id) REFERENCES events(id)  
        )
    ''')

    conn.commit()  # Commit the changes to the database
    conn.close()  # Close the database connection

# Call the function to initialize the database
create_database()

# Function to add a new member to the 'members' table
def add_member(first_name, last_name, d100_number, nsbe_id, email):
    conn = sqlite3.connect('NSBE.db')  # Connect to the database
    c = conn.cursor()  # Create a cursor object to interact with the database

    # Insert a new member with provided details, set dues_paid to False and attendance_count to 0
    c.execute('''
        INSERT INTO members (first_name, last_name, d100_number, nsbe_id, email, dues_paid, attendance_count)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (first_name, last_name, d100_number, nsbe_id, email, False, 0))  # Parameters are passed securely

    conn.commit()  # Commit the changes to the database
    conn.close()  # Close the database connection

# Function to mark dues as paid for a member by their member_id
def pay_dues(member_id):
    conn = sqlite3.connect('NSBE.db')  # Connect to the database
    c = conn.cursor()  # Create a cursor object to interact with the database

    # Update the 'dues_paid' field to True for the given member_id
    c.execute('''
        UPDATE members
        SET dues_paid = ?
        WHERE id = ?
    ''', (True, member_id))  # Parameters are passed securely

    conn.commit()  # Commit the changes to the database
    conn.close()  # Close the database connection

# Function to record attendance for a member at a particular event
def record_attendance(member_id, event_id, attended):
    conn = sqlite3.connect('NSBE.db')  # Connect to the database
    c = conn.cursor()  # Create a cursor object to interact with the database

    # Insert the attendance record into the 'attendance' table
    c.execute('''
        INSERT INTO attendance (member_id, event_id, attended)
        VALUES (?, ?, ?)
    ''', (member_id, event_id, attended))  # Parameters are passed securely

    # If the member attended, increment their attendance count
    if attended:
        c.execute('''
            UPDATE members
            SET attendance_count = attendance_count + 1
            WHERE id = ?
        ''', (member_id,))  # Increment the attendance count for the member

    conn.commit()  # Commit the changes to the database
    conn.close()  # Close the database connection

# Importing tkinter for building the graphical user interface (GUI)
import tkinter as tk
from tkinter import messagebox  # For displaying pop-up messages

# Class to define the GUI for the application
class NSBEApp:
    def __init__(self, root):
        self.root = root  # Store the root window reference
        self.root.title("NSBE Member Tracker")  # Set the window title
        self.root.geometry("600x400")  # Set the window size

        # Call the method to create the UI elements
        self.create_widgets()

    # Method to create all the UI elements (labels, buttons, text entries)
    def create_widgets(self):
        # Add Member section
        self.add_member_label = tk.Label(self.root, text="Add New Member:")
        self.add_member_label.grid(row=0, column=0, columnspan=2)

        self.first_name_label = tk.Label(self.root, text="First Name")
        self.first_name_label.grid(row=1, column=0)
        self.first_name_entry = tk.Entry(self.root)
        self.first_name_entry.grid(row=1, column=1)

        self.last_name_label = tk.Label(self.root, text="Last Name")
        self.last_name_label.grid(row=2, column=0)
        self.last_name_entry = tk.Entry(self.root)
        self.last_name_entry.grid(row=2, column=1)

        self.d100_number_label = tk.Label(self.root, text="D100 Number")
        self.d100_number_label.grid(row=3, column=0)
        self.d100_number_entry = tk.Entry(self.root)
        self.d100_number_entry.grid(row=3, column=1)

        self.nsbe_id_label = tk.Label(self.root, text="NSBE ID")
        self.nsbe_id_label.grid(row=4, column=0)
        self.nsbe_id_entry = tk.Entry(self.root)
        self.nsbe_id_entry.grid(row=4, column=1)

        self.email_label = tk.Label(self.root, text="Email")
        self.email_label.grid(row=5, column=0)
        self.email_entry = tk.Entry(self.root)
        self.email_entry.grid(row=5, column=1)

        self.add_member_button = tk.Button(self.root, text="Add Member", command=self.add_member)
        self.add_member_button.grid(row=6, column=0, columnspan=2)

        # Pay Dues section
        self.pay_dues_label = tk.Label(self.root, text="Pay Dues:")
        self.pay_dues_label.grid(row=7, column=0, columnspan=2)

        self.member_id_label = tk.Label(self.root, text="Member ID")
        self.member_id_label.grid(row=8, column=0)
        self.member_id_entry = tk.Entry(self.root)
        self.member_id_entry.grid(row=8, column=1)

        self.pay_dues_button = tk.Button(self.root, text="Pay Dues", command=self.pay_dues)
        self.pay_dues_button.grid(row=9, column=0, columnspan=2)

        # Record Attendance section
        self.record_attendance_label = tk.Label(self.root, text="Record Attendance:")
        self.record_attendance_label.grid(row=10, column=0, columnspan=2)

        self.event_id_label = tk.Label(self.root, text="Event ID")
        self.event_id_label.grid(row=11, column=0)
        self.event_id_entry = tk.Entry(self.root)
        self.event_id_entry.grid(row=11, column=1)

        self.attendance_label = tk.Label(self.root, text="Attendance (1 for Yes, 0 for No)")
        self.attendance_label.grid(row=12, column=0)
        self.attendance_entry = tk.Entry(self.root)
        self.attendance_entry.grid(row=12, column=1)

        self.record_attendance_button = tk.Button(self.root, text="Record Attendance", command=self.record_attendance)
        self.record_attendance_button.grid(row=13, column=0, columnspan=2)

    # Method to handle adding a new member
    def add_member(self):
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        d100_number = self.d100_number_entry.get()
        nsbe_id = self.nsbe_id_entry.get()
        email = self.email_entry.get()

        # Call the add_member function to add the new member to the database
        add_member(first_name, last_name, d100_number, nsbe_id, email)

        # Display a success message
        messagebox.showinfo("Success", "Member added successfully!")

    # Method to handle paying dues for a member
    def pay_dues(self):
        member_id = int(self.member_id_entry.get())  # Get member ID from input

        # Call the pay_dues function to mark the dues as paid
        pay_dues(member_id)
        # Display a success message
        messagebox.showinfo("Success", "Dues")   # Display a success message
        messagebox.showinfo("Success", "Dues paid successfully!")

    # Method to handle recording attendance for a member at an event
    def record_attendance(self):
        # Get member ID, event ID, and attendance status from the input fields
        member_id = int(self.member_id_entry.get())
        event_id = int(self.event_id_entry.get())
        attended = bool(int(self.attendance_entry.get()))  # Convert 1/0 to True/False

        # Call the record_attendance function to log the attendance in the database
        record_attendance(member_id, event_id, attended)

        # Display a success message
        messagebox.showinfo("Success", "Attendance recorded successfully!")

# Code to run the application
if __name__ == "__main__":
    root = tk.Tk()  # Create the main Tkinter window
    app = NSBEApp(root)  # Initialize the application class
    root.mainloop()  # Start the Tkinter event loop to display the GUI



'''RESOURCES:
Python Documentation:
core syntax and libraries: Python Docs
SQLite Documentation:
SQLite in Python: For working with SQLite databases in Python using the sqlite3 library.
 Core Concepts and Python Libraries Used:
SQLite3 Module: This is the Python interface to SQLite, used to manage the creation, querying, and updating of the database. It allows you to run SQL queries directly from Python to manipulate the database.

Methods used: sqlite3.connect(), cursor(), execute(), commit(), close()
Tkinter Module: This is used for creating a window and handling user interaction (e.g., buttons, text fields). Tkinter allows the creation of GUI components for adding members, marking dues as paid, and recording attendance.

Methods used: Tk(), Label(), Entry(), Button(), grid(), messagebox.showinfo()
Python Control Flow: The use of if statements to control logic (e.g., marking dues as paid, incrementing attendance count) and function definitions to modularize the code.

5. Python Data Types and Structures:
Strings: For storing member details like names, email addresses, D100 numbers, and NSBE IDs.
Booleans: Used to track payment status (dues_paid) and attendance (attended).
Integers: For things like attendance count and event IDs.
6. SQL (Structured Query Language):
SQL is used to interact with the SQLite database. Basic SQL commands like CREATE TABLE, INSERT INTO, UPDATE, and SELECT are used to manage the data in the database.

SQL Commands:

CREATE TABLE: Creates tables to store member, event, and attendance data.
INSERT INTO: Inserts new data into the tables (e.g., adding members).
UPDATE: Modifies data in the tables (e.g., marking dues as paid, recording attendance).
SELECT: Fetches data from the tables for querying (though not used in the provided code, this could be added for listing members or checking attendance).
7. User Interface Design:
The design is kept simple using Tkinter's grid layout system, which places widgets (like labels, entry fields, and buttons) in rows and columns.
Messagebox: Used to display confirmation dialogs (like "Member added successfully") after actions are performed, improving user experience.
8. File Handling:
SQLite Database File: The database file organization.db is created automatically when the script is run. It is a local file stored in the same directory as the Python script, which is used to store all member, attendance, and dues information.'''

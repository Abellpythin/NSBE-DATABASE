'''
This user-friendly application is designed to help organizations efficiently manage member information, 
track national dues payments, and monitor attendance at events. 
The app allows members to register by entering their personal details—such as first name, last name, D100 number, 
NSBE ID, and email; which are securely stored in a centralized database.

'''

import sqlite3

def create_database():
    conn = sqlite3.connect('NSBE.db')
    c = conn.cursor()

    # Create table for members
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

    # Create table for events/attendance
    c.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_name TEXT,
            event_date TEXT
        )
    ''')

    # Create table to track attendance at events
    c.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            member_id INTEGER,
            event_id INTEGER,
            attended BOOLEAN,
            FOREIGN KEY(member_id) REFERENCES members(id),
            FOREIGN KEY(event_id) REFERENCES events(id)
        )
    ''')

    conn.commit()
    conn.close()

create_database()

def add_member(first_name, last_name, d100_number, nsbe_id, email):
    conn = sqlite3.connect('NSBE.db')
    c = conn.cursor()

    # Default attendance count is 0 and dues unpaid by default
    c.execute('''
        INSERT INTO members (first_name, last_name, d100_number, nsbe_id, email, dues_paid, attendance_count)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (first_name, last_name, d100_number, nsbe_id, email, False, 0))

    conn.commit()
    conn.close()

def pay_dues(member_id):
    conn = sqlite3.connect('NSBE.db')
    c = conn.cursor()

    # Mark dues as paid
    c.execute('''
        UPDATE members
        SET dues_paid = ?
        WHERE id = ?
    ''', (True, member_id))

    conn.commit()
    conn.close()

def record_attendance(member_id, event_id, attended):
    conn = sqlite3.connect('NSBE.db')
    c = conn.cursor()

    # Record attendance for a member at an event
    c.execute('''
        INSERT INTO attendance (member_id, event_id, attended)
        VALUES (?, ?, ?)
    ''', (member_id, event_id, attended))

    # Update the attendance count for the member
    if attended:
        c.execute('''
            UPDATE members
            SET attendance_count = attendance_count + 1
            WHERE id = ?
        ''', (member_id,))

    conn.commit()
    conn.close()
import tkinter as tk
from tkinter import messagebox

class NSBEApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NSBE Member Tracker")
        self.root.geometry("600x400")
        
        # UI Elements
        self.create_widgets()

    def create_widgets(self):
        # Add member section
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

        # Pay dues section
        self.pay_dues_label = tk.Label(self.root, text="Pay Dues:")
        self.pay_dues_label.grid(row=7, column=0, columnspan=2)

        self.member_id_label = tk.Label(self.root, text="Member ID")
        self.member_id_label.grid(row=8, column=0)
        self.member_id_entry = tk.Entry(self.root)
        self.member_id_entry.grid(row=8, column=1)

        self.pay_dues_button = tk.Button(self.root, text="Pay Dues", command=self.pay_dues)
        self.pay_dues_button.grid(row=9, column=0, columnspan=2)

        # Attendance section
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

    def add_member(self):
        # Get values from the UI
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        d100_number = self.d100_number_entry.get()
        nsbe_id = self.nsbe_id_entry.get()
        email = self.email_entry.get()

        # Add member to the database
        add_member(first_name, last_name, d100_number, nsbe_id, email)

        messagebox.showinfo("Success", "Member added successfully!")

    def pay_dues(self):
        # Get member ID from the UI
        member_id = int(self.member_id_entry.get())

        # Pay dues for the member
        pay_dues(member_id)

        messagebox.showinfo("Success", "Dues paid successfully!")

    def record_attendance(self):
        # Get values from the UI
        member_id = int(self.member_id_entry.get())
        event_id = int(self.event_id_entry.get())
        attended = bool(int(self.attendance_entry.get()))

        # Record attendance
        record_attendance(member_id, event_id, attended)

        messagebox.showinfo("Success", "Attendance recorded successfully!")

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = NSBEApp(root)
    root.mainloop()

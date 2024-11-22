import sqlite3
import tkinter as tk
from tkinter import messagebox

# Database functions
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

    # Check if the member exists
    c.execute('SELECT * FROM members WHERE id = ?', (member_id,))
    member = c.fetchone()
    if not member:
        return "Member not found"

    # Check if the event exists
    c.execute('SELECT * FROM events WHERE id = ?', (event_id,))
    event = c.fetchone()
    if not event:
        return "Event not found"

    # Record attendance for a member at an event
    c.execute('''
        INSERT INTO attendance (member_id, event_id, attended)
        VALUES (?, ?, ?)
    ''', (member_id, event_id, attended))

    # Update the attendance count for the member if they attended
    if attended:
        c.execute('''
            UPDATE members
            SET attendance_count = attendance_count + 1
            WHERE id = ?
        ''', (member_id,))

    conn.commit()
    conn.close()

    return "Attendance recorded successfully!"

# UI Code
class NSBEApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NSBE Member Tracker")
        self.root.geometry("800x600")

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

        # Admin Access Button (hidden from members)
        self.admin_access_button = tk.Button(self.root, text="Admin Login", command=self.show_admin_login)
        self.admin_access_button.grid(row=7, column=0, columnspan=2)

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

    def show_admin_login(self):
        # Open admin login window
        self.admin_window = tk.Toplevel(self.root)
        self.admin_window.title("Admin Login")
        self.admin_window.geometry("300x200")

        self.password_label = tk.Label(self.admin_window, text="Enter Admin Password:")
        self.password_label.pack(pady=10)

        self.password_entry = tk.Entry(self.admin_window, show="*")
        self.password_entry.pack(pady=10)

        self.login_button = tk.Button(self.admin_window, text="Login", command=self.verify_admin_password)
        self.login_button.pack(pady=10)

    def verify_admin_password(self):
        # Set a simple admin password (this can be made more secure)
        admin_password = "admin123"

        if self.password_entry.get() == admin_password:
            messagebox.showinfo("Success", "Logged in successfully!")
            self.admin_window.destroy()
            self.open_admin_dashboard()
        else:
            messagebox.showerror("Error", "Incorrect password")

    def open_admin_dashboard(self):
        # Open the admin dashboard in a separate window
        self.admin_dashboard = tk.Toplevel(self.root)
        self.admin_dashboard.title("Admin Dashboard")
        self.admin_dashboard.geometry("800x600")

        self.view_members_button = tk.Button(self.admin_dashboard, text="View Members", command=self.view_members)
        self.view_members_button.pack(pady=20)

        self.view_attendance_button = tk.Button(self.admin_dashboard, text="View Attendance", command=self.view_attendance)
        self.view_attendance_button.pack(pady=20)

        self.view_events_button = tk.Button(self.admin_dashboard, text="View Events", command=self.view_events)
        self.view_events_button.pack(pady=20)

    def view_members(self):
        conn = sqlite3.connect('NSBE.db')
        c = conn.cursor()

        # Get all members
        c.execute('SELECT * FROM members')
        members = c.fetchall()

        # Display the list of members
        members_list = "\n".join([f"{member[0]}: {member[1]} {member[2]} - {member[4]}" for member in members])

        # Show members in a messagebox (or use a Text widget for larger content)
        messagebox.showinfo("Members", members_list)
        conn.close()

    def view_attendance(self):
        conn = sqlite3.connect('NSBE.db')
        c = conn.cursor()

        # Get all attendance records
        c.execute('''
            SELECT a.member_id, m.first_name, m.last_name, e.event_name, a.attended
            FROM attendance a
            JOIN members m ON a.member_id = m.id
            JOIN events e ON a.event_id = e.id
        ''')
        attendance = c.fetchall()

        # Display the list of attendance records
        attendance_list = "\n".join([f"{att[1]} {att[2]} - {att[3]}: {'Attended' if att[4] else 'Did not attend'}" for att in attendance])

        # Show attendance records in a messagebox
        messagebox.showinfo("Attendance Records", attendance_list)
        conn.close()

    def view_events(self):
        conn = sqlite3.connect('NSBE.db')
        c = conn.cursor()

        # Get all events
        c.execute('SELECT * FROM events')
        events = c.fetchall()

        # Display the list of events
        events_list = "\n".join([f"{event[0]}: {event[1]} on {event[2]}" for event in events])

        # Show events in a messagebox
        messagebox.showinfo("Events", events_list)
        conn.close()

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = NSBEApp(root)
    root.mainloop()
'''
Admin Login: The show_admin_login method displays a password prompt. If the password matches (e.g., "admin123"), the admin gets access to the admin dashboard.

Admin Dashboard: Once logged in, the admin can access three functions:

View Members (view_members): Displays the list of members.
View Attendance (view_attendance): Displays all attendance records with member and event information.
View Events (view_events): Displays a list of events.
Separation of Access: The admin access is completely separate from the member-facing UI. Regular users won’t be able to see or access the admin section.

Security: The admin login uses a simple password. For production purposes, you'd want a more secure authentication system.

he ability to view and interact with the database separately from the member-facing UI (with exclusive access for administrative purposes), you can create a backend admin interface or a separate admin tool for managing and viewing the database.

This can be done by creating an admin-only access panel that is protected from regular users, and you can hide this admin access from the member-facing part of the app. Below is an approach where:

The admin interface will have a password prompt for extra security.
You will be able to view the members, attendance, and event data in a separate UI window when authenticated.
How to Implement Admin Access:
Admin Login Panel: A login screen where an admin enters a password to access the admin section.
Admin Dashboard: A separate window or section that only the admin can access, displaying data such as members, dues, attendance, and events.

 make a session for admin and non admin

'''
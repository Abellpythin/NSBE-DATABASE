import sqlite3
import tkinter as tk
from tkinter import messagebox

# Database Setup
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

# Function to add a new member
def add_member(first_name, last_name, d100_number, nsbe_id, email):
    conn = sqlite3.connect('NSBE.db')
    c = conn.cursor()

    # Insert the new member with default values for dues and attendance
    c.execute('''
        INSERT INTO members (first_name, last_name, d100_number, nsbe_id, email, dues_paid, attendance_count)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (first_name, last_name, d100_number, nsbe_id, email, False, 0))

    conn.commit()
    conn.close()

# Function to mark dues as paid
def pay_dues(member_id):
    conn = sqlite3.connect('NSBE.db')
    c = conn.cursor()

    # Update the dues_paid field for the given member ID
    c.execute('''
        UPDATE members
        SET dues_paid = ?
        WHERE id = ?
    ''', (True, member_id))

    conn.commit()
    conn.close()

# Function to record attendance for an event
def record_attendance(member_id, event_id, attended):
    conn = sqlite3.connect('NSBE.db')
    c = conn.cursor()

    # Record attendance in the attendance table
    c.execute('''
        INSERT INTO attendance (member_id, event_id, attended)
        VALUES (?, ?, ?)
    ''', (member_id, event_id, attended))

    # If attended, increment the attendance count for the member
    if attended:
        c.execute('''
            UPDATE members
            SET attendance_count = attendance_count + 1
            WHERE id = ?
        ''', (member_id,))

    conn.commit()
    conn.close()

# Admin Access & UI
class NSBEApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NSBE Member Tracker")
        self.root.geometry("800x600")
        self.create_widgets()

    def create_widgets(self):
        # Login for admin
        self.admin_button = tk.Button(self.root, text="Admin Login", command=self.show_admin_login)
        self.admin_button.pack(pady=20)

        # Add Member Section
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

        # Pay dues Section
        self.pay_dues_label = tk.Label(self.root, text="Pay Dues:")
        self.pay_dues_label.grid(row=7, column=0, columnspan=2)

        self.member_id_label = tk.Label(self.root, text="Member ID")
        self.member_id_label.grid(row=8, column=0)
        self.member_id_entry = tk.Entry(self.root)
        self.member_id_entry.grid(row=8, column=1)

        self.pay_dues_button = tk.Button(self.root, text="Pay Dues", command=self.pay_dues)
        self.pay_dues_button.grid(row=9, column=0, columnspan=2)

        # Record Attendance Section
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

    def show_admin_login(self):
        # Admin login for exclusive access
        self.admin_window = tk.Toplevel(self.root)
        self.admin_window.title("Admin Login")
        self.admin_window.geometry("300x200")
        
        self.password_label = tk.Label(self.admin_window, text="Enter Admin Password:")
        self.password_label.pack(pady=10)
        
        self.password_entry = tk.Entry(self.admin_window, show="*")
        self.password_entry.pack(pady=5)
        
        self.login_button = tk.Button(self.admin_window, text="Login", command=self.verify_admin_password)
        self.login_button.pack(pady=10)

    def verify_admin_password(self):
        admin_password = "admin123"  # Simple password for admin
        if self.password_entry.get() == admin_password:
            messagebox.showinfo("Success", "Logged in successfully!")
            self.admin_window.destroy()
            self.open_admin_dashboard()
        else:
            messagebox.showerror("Error", "Incorrect password")

    def open_admin_dashboard(self):
        # Dashboard for admin after successful login
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
        c.execute('SELECT * FROM members')
        members = c.fetchall()
        members_list = "\n".join([f"{member[0]}: {member[1]} {member[2]} - {member[4]}" for member in members])
        messagebox.showinfo("Members", members_list)
        conn.close()

    def view_attendance(self):
        conn = sqlite3.connect('NSBE.db')
        c = conn.cursor()
        c.execute('''
            SELECT members.first_name, members.last_name, events.event_name, attendance.attended
            FROM attendance
            JOIN members ON attendance.member_id = members.id
            JOIN events ON attendance.event_id = events.id
        ''')
        attendance = c.fetchall()
        attendance_list = "\n".join([f"{att[0]} {att[1]} attended {att[2]}: {'Attended' if att[3] else 'Did not attend'}" for att in attendance])
        messagebox.showinfo("Attendance Records", attendance_list)
        conn.close()

    def view_events(self):
        conn = sqlite3.connect('NSBE.db')
        c = conn.cursor()
        c.execute('SELECT * FROM events')
        events = c.fetchall()
        events_list = "\n".join([f"{event[0]}: {event[1]} on {event[2]}" for event in events])
        messagebox.showinfo("Events", events_list)
        conn.close()

    def add_member(self):
        # Get data from UI and add member to database
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        d100_number = self.d100_number_entry.get()
        nsbe_id = self.nsbe_id_entry.get()
        email = self.email_entry.get()

        add_member(first_name, last_name, d100_number, nsbe_id, email)
        messagebox.showinfo("Success", "Member added successfully!")

    def pay_dues(self):
        # Get member ID and pay dues
        member_id = int(self.member_id_entry.get())
        pay_dues(member_id)
        messagebox.showinfo("Success", "Dues paid successfully!")

    def record_attendance(self):
        # Get attendance data and record it
        member_id = int(self.member_id_entry.get())
        event_id = int(self.event_id_entry.get())
        attended = bool(int(self.attendance_entry.get()))
        record_attendance(member_id, event_id, attended)
        messagebox.showinfo("Success", "Attendance recorded successfully!")

# Create the database and start the Tkinter app
if __name__ == "__main__":
    create_database()  # Create the database if it doesn't exist
    root = tk.Tk()
    app = NSBEApp(root)
    root.mainloop()
'''
Database Creation: The create_database function sets up tables for members, events, and attendance tracking.
Admin Login: Admins can access exclusive features (viewing members, events, attendance) via an admin password.
Member Interaction: Members can add their information, pay dues, and record attendance through the UI.
Admin Dashboard: Once logged in, admins can view all members, event attendance, and event details.

'''
'''
This user-friendly application is designed to help organizations efficiently manage member information, 
track national dues payments, and monitor attendance at events. 
The app allows members to register by entering  their personal details—such as first name, last name, 
D100 number, NSBE ID, and email;
which are securely stored in a centralized database.

'''


'''Added implementation:
    - ability to remove and delete
    - add hours and attendance
    - payments (national and chapter)
    - events 
        '''
        
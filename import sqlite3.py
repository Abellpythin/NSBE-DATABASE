import sqlite3
def create_database():
    conn = sqlite3.connect('.db')
    c = conn.cursor()
    # Create table for members
    c.execute('''
            CREATE TABLE IF NOT EXISTS members(
              id INTERGER PRIMARY KEY AUTOINCREMENNT,
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
        CREATE TABLE IF NOT EXISTS events(
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              event_name TEXT,
              event_date TEXT
              )
        ''')
    # Create table to track attendance at evnts
    c.execute('''
        CREATE TABLE IF NOT EXISTS attendance(
            member_id INTEGER,
            event_id INTEGER,
              attendance BOOLEAN,
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

    # default attendace count is 0 and dues unpaid by default
    c.execute('''
        INSERT INTO members (first_name, last_name, d100_number, nsbe_id, email, dues_paid, attendace_count)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (first_name, last_name, d100_number, nsbe_id, email, False, 0))
    conn.commit()
    conn.close()

def pay_dues(member_id):
    conn = sqlite3.connect('NSBE.db')
    c = conn.cursor

    # Mark dues as paid
    c.execute('''
        UPDATE members
        SET dues_paid = ?
        WHERE id = ?
    ''', (True, member_id))
    conn.commit()
    conn.close()

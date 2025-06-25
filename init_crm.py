import sqlite3

conn = sqlite3.connect("CRM.db")
c = conn.cursor()
c.execute('''
CREATE TABLE IF NOT EXISTS customers(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT NOT NULL,
          email TEXT NOT NULL UNIQUE,
          phone text,
          note TEXT
          )''')

conn.commit()
conn.close()
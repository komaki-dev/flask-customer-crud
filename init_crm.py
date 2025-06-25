import sqlite3

conn = sqlite3.connect("CRM.db")
c = conn.cursor()
c.execute('''
CREATE TABLE IF NOT EXISTS customers(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT NOT NULL,
          email TEXT NOT NULL UNIQUE,
          phone text,
          note TEXT,
          deleted INTEGER DEFAULT 0
          )''')

conn.commit()
conn.close()
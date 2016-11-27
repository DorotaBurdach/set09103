import sqlite3

conn = sqlite3.connect("books.db")

cursor = conn.cursor()

# create a table
cursor.execute("""CREATE TABLE mail
                  (id INTEGER PRIMARY KEY, name text, email text, title text, message text, page text)
               """)

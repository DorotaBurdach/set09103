import sqlite3

conn = sqlite3.connect("books.db")

cursor = conn.cursor()

# create a table
cursor.execute("""CREATE TABLE new
                  (id INTEGER PRIMARY KEY, title text, author text, desc text, img text)
               """)

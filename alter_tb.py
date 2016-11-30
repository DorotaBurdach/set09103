import sqlite3

conn = sqlite3.connect("books.db")

cursor = conn.cursor()

# create a table
cursor.execute(""" ALTER TABLE books ADD ip text """)
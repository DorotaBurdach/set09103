import sqlite3
 
conn = sqlite3.connect("books.db") # or use :memory: to put it in RAM
 
cursor = conn.cursor()

# insert some data
cursor.execute(" DROP TABLE IF EXISTS books;")
 
# save data to database
conn.commit()
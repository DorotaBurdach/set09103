import sqlite3

conn = sqlite3.connect("books.db")

cursor = conn.cursor()

# create a table
cursor.execute("""CREATE TABLE books
                  (id INTEGER PRIMARY KEY, p_name text, p_surname text, p_desc text, p_img text, path_status text, path_desc text, b1_title text, b1_author text, b1_img text, b1_desc text, b2_title text, b2_author text, b2_img text, b2_desc text, b3_title text, b3_author text, b3_img text, b3_desc text, b4_title text, b4_author text, b4_img text, b4_desc text, b5_title text, b5_author text, b5_img text, b5_desc text)
               """)

import sqlite3

# connects me to sql
def create_db():
    conn = sqlite3.connect('resumes.db') # creates the file if it DNE
    c = conn.cursor() # conn creates the connection from SQL to python, .cursor() allows me to execute sql commands

    # creates table for resumes if it doesnt exist already
    c.execute('''CREATE TABLE IF NOT EXISTS resumes (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              email TEXT,
              phone TEXT,
              linkedin TEXT,
              skills TEXT,
              experience TEXT,
              education TEXT,
              resume_text TEXT
              )''')
    conn.commit() # save canges to db
    conn.close() # close the connection


# run the def to create db and table
create_db()
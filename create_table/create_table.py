import sqlite3


def create_table():
  with sqlite3.connect("database.db") as db:
    cursor = db.cursor()

  query = """
    CREATE TABLE IF NOT EXISTS phone_directory(    
      id INTEGER PRIMARY KEY,
      phone_number VARCHAR(20) NOT NULL,
      firstname VARCHAR(50) NOT NULL,
      lastname VARCHAR(50) NOT NULL
    );
  """

  cursor.executescript(query)
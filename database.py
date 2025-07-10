import sqlite3

def get_connection():
    conn = sqlite3.connect("ecommerce.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS products(
                   id integer primary key autoincrement,
                   name varchar(200) not null,
                   price float not null,
                   stock integer
                   )
                   """)
    conn.commit()
    conn.close()
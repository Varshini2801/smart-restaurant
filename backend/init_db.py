# backend/init_db.py
import sqlite3
import os

def create_tables_and_data():
    db_path = 'backend/database.db'
    os.makedirs('backend', exist_ok=True)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute('CREATE TABLE IF NOT EXISTS menu (id INTEGER PRIMARY KEY, item TEXT, price REAL)')
    c.execute('CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY, table_id TEXT, items TEXT, total REAL)')

    # Add sample data if menu is empty
    c.execute('SELECT COUNT(*) FROM menu')
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO menu (item, price) VALUES ('Pizza', 8.5), ('Burger', 5.0), ('Pasta', 6.5)")

    conn.commit()
    conn.close()


import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

c.execute('CREATE TABLE IF NOT EXISTS menu (id INTEGER PRIMARY KEY, item TEXT, price REAL)')
c.execute('CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY, table_id TEXT, items TEXT, total REAL)')

# Add menu items
c.execute("INSERT INTO menu (item, price) VALUES ('Pizza', 8.5), ('Burger', 5.0), ('Pasta', 6.5)")
conn.commit()
conn.close()

from flask import Flask, request, jsonify, render_template
import sqlite3
from flask_cors import CORS
from collections import Counter
import ast
import os

# Absolute path to database
DB_PATH = os.path.join(os.path.dirname(__file__), 'database.db')

# Initialize DB if it doesn't exist
if not os.path.exists(DB_PATH):
    from init_db import create_tables_and_data
    create_tables_and_data()

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analytics-page')
def analytics_page():
    return render_template('analytics.html')

@app.route('/menu', methods=['GET'])
def get_menu():
    db = get_db()
    items = db.execute('SELECT * FROM menu').fetchall()
    return jsonify([dict(i) for i in items])

@app.route('/order', methods=['POST'])
def place_order():
    data = request.json
    db = get_db()
    db.execute('INSERT INTO orders (table_id, items, total) VALUES (?, ?, ?)',
               (data['table_id'], str(data['items']), data['total']))
    db.commit()
    return jsonify({'message': 'Order placed'}), 201

@app.route('/analytics', methods=['GET'])
def analytics():
    db = get_db()
    orders = db.execute('SELECT items, total FROM orders').fetchall()

    all_items = []
    total_income = 0.0

    for order in orders:
        try:
            items = ast.literal_eval(order['items'])
            all_items.extend(items)
            total_income += order['total']
        except Exception as e:
            print("Error parsing order:", order['items'], e)

    item_counts = Counter(all_items)
    tax_rate = 0.05
    tax_collected = total_income * tax_rate / (1 + tax_rate)

    return jsonify({
        'most_ordered': item_counts.most_common(),
        'total_income': total_income,
        'tax_collected': tax_collected
    })

if __name__ == '__main__':
    app.run(debug=True)

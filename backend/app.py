from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS
from collections import Counter
import ast

app = Flask(__name__)
CORS(app)

def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# ✅ Home route for base URL
@app.route('/')
def index():
    return '''
        <h1>Restaurant Ordering API</h1>
        <p>Available endpoints:</p>
        <ul>
            <li><strong>GET</strong> /menu - Get menu items</li>
            <li><strong>POST</strong> /order - Place a new order</li>
            <li><strong>GET</strong> /analytics - View analytics</li>
        </ul>
    '''

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

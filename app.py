from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
#from prometheus_client import generate_latest
import time

app = Flask(__name__)

# MySQL configuration
app.config['MYSQL_HOST'] = '192.168.16.19'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL-PASSWORD'] ='lougrace'
app.config['MYSQL_DB'] = 'ecommerce'

mysql = MySQL(app)

@app.route('/products', methods=['GET'])
def get_products():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products")
    rows = cur.fetchall()
    cur.close()
    products = [{'id': row[0], 'name': row[1], 'price': row[2], 'stock': row[3]} for row in rows]
    return jsonify(products)

@app.route('/order', methods=['POST'])
def place_order():
    product_id = request.json['product_id']
    quantity = request.json['quantity']

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO orders (products_id, quantity) VALUES (%s, %s)", (product_id, quantity))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'Order placed successfully'}), 201

#@app.route('/metrics', methods=['GET'])
#def metrics():
#    return generate_latest(), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
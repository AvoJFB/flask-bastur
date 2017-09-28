from app import app, models, db
from datetime import datetime
from flask import request, jsonify


@app.route('/customer', methods=['POST'])
def create_customer():
    new_customer = models.Customer(request.get_json().get('name'))
    db.session.add(new_customer)
    db.session.commit()

    return jsonify({
        "message": "OK"
    })


@app.route('/customer', methods=['GET'])
def get_customers():
    customers = models.Customer.query.all()
    return jsonify({
        "customers": [customer.serialize for customer in customers]
    })


@app.route('/order', methods=['POST'])
def create_order():
    params = request.get_json()
    new_order = models.Order(
        params.get('customer_id'),
        params.get('weight'),
        params.get('price_per_kilo'),
        datetime.now()
    )
    db.session.add(new_order)
    db.session.commit()

    return jsonify({
        "message": "OK"
    })


@app.route('/order', methods=['GET'])
def get_orders():
    orders = models.Order.query.all()
    return jsonify({
        "orders": [order.serialize for order in orders]
    })

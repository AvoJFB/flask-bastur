from app import db


class Customer(db.Model):
    __tablename__ = 'customers'
    customer_id = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    orders = db.relationship("Order", back_populates="customer")

    @property
    def serialize(self):
        return {
            'id': self.customer_id,
            'name': self.name,
            'orders': [order.serialize_without_customer for order in self.orders]
        }

    def __init__(self, name):
        self.name = name


class Order(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key=True)
    customer_id = db.Column(db.ForeignKey('customers.customer_id'))
    customer = db.relationship("Customer", back_populates="orders")
    weight = db.Column(db.Float)
    price_per_kilo = db.Column(db.Integer)
    sold_at = db.Column(db.Date)

    @property
    def serialize(self):
        return {
            'id': self.order_id,
            'customer': {
                'id': self.customer.customer_id,
                'name': self.customer.name
            },
            'weight': self.weight,
            'price_per_kilo': self.price_per_kilo,
            'sold_at': self.sold_at,
            'summary': int(self.weight * self.price_per_kilo)
        }

    @property
    def serialize_without_customer(self):
        return {
            'id': self.order_id,
            'weight': self.weight,
            'price_per_kilo': self.price_per_kilo,
            'sold_at': self.sold_at,
            'summary': int(self.weight * self.price_per_kilo)
        }

    def __init__(self, customer_id, weight, price_per_kilo, sold_at):
        self.customer_id = customer_id
        self.weight = weight
        self.price_per_kilo = price_per_kilo
        self.sold_at = sold_at

from src import db


class Purchases(db.Model):
    __tablename__ = "purchases"

    purchase_id = db.Column(db.Integer, primary_key = True)
    purchase_date = db.Column(db.Date, nullable=False)
    number_of_purchases = db.Column(db.Integer, nullable = False)

    product_id = db.Column(db.Integer, db.ForeignKey("products.product_id", onupdate="CASCADE", ondelete="CASCADE"), nullable = False)

    def __init__(self, purchase_date, product_id, number_of_purchases=1):
        self.purchase_date = purchase_date
        self.number_of_purchases = number_of_purchases
        self.product_id = product_id


class Products(db.Model):
    __tablename__ = "products"

    product_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30), nullable = False)
    price = db.Column(db.Numeric(10.2), nullable = False)
    manufacturer = db.Column(db.String(30), nullable = False)
    
    purchases = db.relationship("Purchases", backref = "products", lazy="dynamic")

    def __init__(self, name, price, manufacturer):
        self.name = name
        self.price = price
        self.manufacturer = manufacturer
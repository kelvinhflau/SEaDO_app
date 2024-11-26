from datetime import datetime
from src import User, Products, Purchases
from src import app, db

app.app_context().push()

Purchases.query.delete()
User.query.delete()
Products.query.delete()


users = [
    User(username="admin", password="admin", is_admin=True),
    User(username="user1", password="user1"),
    User(username="user2", password="user2")
]

product01 = Products(name="Laptop", price = 1100, manufacturer= "Lenovo")
product02 = Products(name="Desktop", price = 2000.12, manufacturer="Dell")
product03 = Products(name="Desktop 2", price = 200, manufacturer="Apple")
product04 = Products(name="Desktop 3", price = 3400, manufacturer="HP")

products = [
    product01,
    product02,
    product03,
    product04
]

db.session.add_all(users)
db.session.add_all(products)
db.session.commit()

purchases = [
    Purchases(purchase_date=datetime.strptime("03/01/2020", "%d/%m/%Y").date(), number_of_purchases=1, product_id=1),
    Purchases(purchase_date=datetime.strptime("04/02/2020", "%d/%m/%Y").date(), number_of_purchases=2, product_id=1),
    Purchases(purchase_date=datetime.strptime("13/03/2020", "%d/%m/%Y").date(), number_of_purchases=3, product_id=2),
    Purchases(purchase_date=datetime.strptime("23/05/2020", "%d/%m/%Y").date(), number_of_purchases=4, product_id=3),
    Purchases(purchase_date=datetime.strptime("03/08/2020", "%d/%m/%Y").date(), number_of_purchases=2, product_id=4)
]


db.session.add_all(purchases)
db.session.commit()
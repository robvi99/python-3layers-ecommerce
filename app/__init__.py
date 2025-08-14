
import os
from flask import Flask
import mysql.connector 
import redis 
import time

from app.models.user import User
from app.models.product import Product
from app.models.category import Category
from app.models.order import Order

from app.services.auth_service import AuthService
from app.services.product_service import ProductService
from app.services.cart_service import CartService
from app.services.order_service import OrderService

from app.routes.auth import create_auth_routes
from app.routes.products import create_products_routes
from app.routes.cart import create_cart_routes
from app.routes.orders import create_orders_routes
from app.routes.admin import create_admin_routes

app = Flask(__name__)
#app.cofig['SECRET_KEY'] = 'secret-key'
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'default_for_dev')

# Database Connections
def connect_mysql():
    for atempt in range(3):
        try:
            conn = mysql.connector.connect(
                host = 'mysql',
                user = 'root',
                password = 'password',
                database = 'ecommerce'
            )
            return conn
        except mysql.connector.Error as err:
            print(f"Error connecting to MySQL: {err}")
            time.sleep(5)
        raise Exception("Failed to connect to MySQL after retries")

mysql_conn = connect_mysql()
redis_client = redis.Redis(host='redis', port=6379, db=0)

# Initialize models
user_model = User(mysql_conn)
product_model = Product(mysql_conn)
category_model = Category(mysql_conn)
order_model = Order(mysql_conn)

# Initialize services
auth_service = AuthService(user_model, redis_client)
product_service = ProductService(product_model, redis_client)
cart_service = CartService(redis_client)
order_service = OrderService(order_model, cart_service, product_model)

# Register blueprints 
app.register_blueprint(create_auth_routes(auth_service))
app.register_blueprint(create_products_routes(product_service))
app.register_blueprint(create_cart_routes(cart_service))
app.register_blueprint(create_orders_routes(order_service))
app.register_blueprint(create_admin_routes(auth_service, product_service, category_model))

# Initialize database schema
with mysql_conn.cursor() as cursor:
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                   id INT AUTO_INCREMENT PRIMARY KEY,
                   username VARCHAR(255) UNIQUE,
                   password VARCHAR(255) NOT NULL,
                   role VARCHAR(50),
                   disabled BOOLEAN DEFAULT FALSE
                   )
                   ''')
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS categories (
                   id INT AUTO_INCREMENT PRIMARY KEY,
                   name VARCHAR(255) UNIQUE
                   )
                   ''')
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS products (
                   id INT AUTO_INCREMENT PRIMARY KEY,
                   name VARCHAR(255) NOT NULL,
                   price DECIMAL(10,2),
                   category_id INT, 
                   FOREIGN KEY (category_id) REFERENCES categories(id)
                   )
                   ''')
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS orders (
                   id INT AUTO_INCREMENT PRIMARY KEY,
                   user_id INT,
                   total DECIMAL(10,2),
                   FOREIGN KEY (user_id) REFERENCES users(id)
                   )
                   ''')
    mysql_conn.commit()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
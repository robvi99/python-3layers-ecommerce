class Product:
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def create_product(self, name, price, category_id):
        with self.db_conn.cursor() as cursor:
            cursor.execute('INSERT INTO products (name, price, category_id) VALUES (%s, %s, %s)',
                           (name, price, category_id))
            self.db_conn.commit()

    def update_product(self, product_id, name, price, category_id):
        with self.db_conn.cursor() as cursor:
            cursor.execute('UPDATE products SET name = %s, price = %s, category_id = %s WHERE id = %s',
                           (name, price, category_id, product_id))
            self.db_conn.commit()

    def delete_product(self, product_id):
        with self.db_conn.cursor() as cursor:
            cursor.execute('DELETE FROM products WHERE id = %s', (product_id,))
            self.db_conn.commit()

    def get_products(self):
        with self.db_conn.cursor(dictionary=True) as cursor:
            cursor.execute('SELECT p.*, c.name as category_name FROM products p JOIN categories c ON p.category_id = c.id')
            return cursor.fetchall()
class Order:
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def create_order(self, user_id, total):
        with self.db_conn.cursor() as cursor:
            cursor.execute('INSERT INTO orders (user_id, total, status) VALUES (%s, %s, %s)',
                           (user_id, total, 'pending'))
            self.db_conn.commit()
            return cursor.lastrowid

    def update_order_status(self, order_id, status):
        with self.db_conn.cursor() as cursor:
            cursor.execute('UPDATE orders SET status = %s WHERE id = %s', (status, order_id))
            self.db_conn.commit()

    def get_orders_by_user(self, user_id):
        with self.db_conn.cursor(dictionary=True) as cursor:
            cursor.execute('SELECT * FROM orders WHERE user_id = %s', (user_id,))
            return cursor.fetchall()
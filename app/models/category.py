class Category:
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def create_category(self, name):
        with self.db_conn.cursor() as cursor:
            cursor.execute('INSERT INTO categories (name) VALUES (%s)', (name,))
            self.db_conn.commit()

    def delete_category(self, category_id):
        with self.db_conn.cursor() as cursor:
            cursor.execute('DELETE FROM categories WHERE id = %s', (category_id,))
            self.db_conn.commit()
import bcrypt

class User:
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def create_user(self, username, password, role):
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        with self.db_conn.cursor() as cursor:
            cursor.execute('INSERT INTO users (username, password, role) VALUES (%s, %s, %s)',
                           (username, hashed, role))
            self.db_conn.commit()

    def get_user_by_username(self, username):
        with self.db_conn.cursor(dictionary=True) as cursor:
            cursor.execute('SELECT * FROM users WHERE username = %s AND disabled = FALSE', (username,))
            return cursor.fetchone()

    def disable_user(self, user_id):
        with self.db_conn.cursor() as cursor:
            cursor.execute('UPDATE users SET disabled = TRUE WHERE id = %s', (user_id,))
            self.db_conn.commit()
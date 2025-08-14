import bcrypt
import json

class AuthService:
    def __init__(self, user_model, redis_client):
        self.user_model = user_model
        self.redis_client = redis_client

    def register(self, username, password, role='customer'):
        existing_user = self.user_model.get_user_by_username(username)
        if existing_user:
            return False, "Username already exists"
        self.user_model.create_user(username, password, role)
        return True, "User registered successfully"

    def login(self, username, password):
        user = self.user_model.get_user_by_username(username)
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            self.redis_client.set(f'session:{username}', json.dumps(user), ex=3600)
            return user
        return None

    def disable_user(self, user_id):
        self.user_model.disable_user(user_id)
        return True
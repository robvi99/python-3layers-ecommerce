import json

class CartService:
    def __init__(self, redis_client):
        self.redis_client = redis_client

    def add_to_cart(self, user_id, product_id, quantity):
        cart_key = f'cart:{user_id}'
        cart = json.loads(self.redis_client.get(cart_key) or '{}')
        cart[str(product_id)] = cart.get(str(product_id), 0) + quantity
        self.redis_client.set(cart_key, json.dumps(cart), ex=86400)
        return True

    def get_cart(self, user_id):
        cart_key = f'cart:{user_id}'
        return json.loads(self.redis_client.get(cart_key) or '{}')

    def clear_cart(self, user_id):
        cart_key = f'cart:{user_id}'
        self.redis_client.delete(cart_key)
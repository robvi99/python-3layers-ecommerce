import json

class ProductService:
    def __init__(self, product_model, redis_client):
        self.product_model = product_model
        self.redis_client = redis_client

    def add_product(self, name, price, category_id):
        self.product_model.create_product(name, price, category_id)
        self.redis_client.delete('products_cache')
        return True

    def update_product(self, product_id, name, price, category_id):
        self.product_model.update_product(product_id, name, price, category_id)
        self.redis_client.delete('products_cache')
        return True

    def delete_product(self, product_id):
        self.product_model.delete_product(product_id)
        self.redis_client.delete('products_cache')
        return True

    def get_products(self):
        cached = self.redis_client.get('products_cache')
        if cached:
            return json.loads(cached)
        products = self.product_model.get_products()
        self.redis_client.set('products_cache', json.dumps(products), ex=300)
        return products
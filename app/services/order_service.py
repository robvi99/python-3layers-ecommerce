class OrderService:
    def __init__(self, order_model, cart_service, product_model):
        self.order_model = order_model
        self.cart_service = cart_service
        self.product_model = product_model

    def place_order(self, user_id):
        cart = self.cart_service.get_cart(user_id)
        products = self.product_model.get_products()
        product_dict = {str(p['id']): p for p in products}
        total = sum(float(product_dict.get(p_id, {'price': 0})['price']) * q for p_id, q in cart.items())
        order_id = self.order_model.create_order(user_id, total)
        self.order_model.update_order_status(order_id, 'completed')
        self.cart_service.clear_cart(user_id)
        return order_id

    def get_order_history(self, user_id):
        return self.order_model.get_orders_by_user(user_id)
from flask import Blueprint, request, render_template, session, redirect, url_for, jsonify

def create_cart_routes(cart_service):
    cart_bp = Blueprint('cart', __name__)

    def login_required(f):
        def wrapper(*args, **kwargs):
            if 'user_id' not in session:
                return redirect(url_for('auth.login'))
            return f(*args, **kwargs)
        wrapper.__name__ = f.__name__
        return wrapper

    @cart_bp.route('/cart', methods=['GET', 'POST'])
    @login_required
    def cart():
        if request.method == 'POST':
            product_id = request.form['product_id']
            quantity = int(request.form['quantity'])
            cart_service.add_to_cart(session['user_id'], product_id, quantity)
        cart_items = cart_service.get_cart(session['user_id'])
        return render_template('cart.html', cart=cart_items)

    @cart_bp.route('/api/cart', methods=['POST'])
    @login_required
    def api_add_to_cart():
        data = request.json
        product_id = data['product_id']
        quantity = data['quantity']
        success = cart_service.add_to_cart(session['user_id'], product_id, quantity)
        return jsonify({'success': success})

    return cart_bp
from flask import Blueprint, session, redirect, url_for, render_template

def create_orders_routes(order_service):
    orders_bp = Blueprint('orders', __name__)

    def login_required(f):
        def wrapper(*args, **kwargs):
            if 'user_id' not in session:
                return redirect(url_for('auth.login'))
            return f(*args, **kwargs)
        wrapper.__name__ = f.__name__
        return wrapper

    @orders_bp.route('/checkout', methods=['POST'])
    @login_required
    def checkout():
        order_id = order_service.place_order(session['user_id'])
        return redirect(url_for('orders.history'))

    @orders_bp.route('/orders')
    @login_required
    def history():
        orders = order_service.get_order_history(session['user_id'])
        return render_template('order_history.html', orders=orders)

    return orders_bp
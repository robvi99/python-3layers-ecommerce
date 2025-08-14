from flask import Blueprint, render_template, session, redirect, url_for, jsonify

def create_products_routes(product_service):
    products_bp = Blueprint('products', __name__)

    def login_required(f):
        def wrapper(*args, **kwargs):
            if 'user_id' not in session:
                return redirect(url_for('auth.login'))
            return f(*args, **kwargs)
        wrapper.__name__ = f.__name__
        return wrapper
    
    @products_bp.route('/')
    @login_required
    def index():
        products = product_service.get_products()
        return render_template('index.html', products=products)
    
    @products_bp.route('/api/products', methods=['GET'])
    @login_required
    def api_products():
        products = product_service.get_products()
        return jsonify(products)
    
    return products_bp

from flask import Blueprint, render_template, session, redirect, url_for, jsonify, request

def create_admin_routes(auth_service, product_service, category_model):
    admin_bp = Blueprint('admin', __name__)

    def admin_required(f):
        def wrapper(*args, **kwargs):
            if 'role' not in session or session['role'] != 'admin':
                return redirect(url_for('auth_login'))
            return f(*args, **kwargs)
        wrapper.__name__ = f.__name__
        return wrapper 
    
    @admin_bp.route('/admin', methods=['GET', 'POST'])
    @admin_required
    def admin():
        if request.method == 'POST':
            action = request.form.get('action')
            try:
                if action =='add_product':
                    product_service.add_product(
                        request.form['name'],
                        float(request.form['price']),
                        int(request.form['category_id'])
                    )
                elif action == 'update_product':
                    product_service.update_product(
                        int(request.form['id']),
                        request.form['name'],
                        float(request.form['price']),
                        int(request.form['category_id'])
                    )
                elif action == 'delete_product':
                    product_service.delete_product(int(request.form['product_id']))
                elif action == 'add_category':
                    category_model.create_category(request.form['name'])
                elif action == 'delete_category':
                    category_model.delete_category(int(request.form['category_id']))
                elif action == 'disable_user':
                    auth_service.disable_user(int(request.form['user_id']))
            except Exception as e:
                return render_template('admin.html', products=product_service.get_products(), error=str(e))
        products = product_service.get_products()
        return render_template('admin.html', products=products)
    
    return admin_bp 

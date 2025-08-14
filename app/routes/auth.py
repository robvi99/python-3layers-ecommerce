from flask import Blueprint, request, redirect, url_for, session, render_template, jsonify 

def create_auth_routes(auth_service):
    auth_bp = Blueprint('auth', __name__)

    @auth_bp.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            success, message = auth_service.register(username, password)
            if success:
                return redirect(url_for('auth.login'))
            return render_template('register.html', error=message)
        return render_template('register.html')

    @auth_bp.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = auth_service.login(username, password)
            if user:
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['role'] = user['role']
                return redirect(url_for('products.index'))
            return render_template('login.html', error="Invalid credentials")
        return render_template('login.html')
    
    @auth_bp.route('/logout')
    def logout():
        for key in ['user_id', 'username', 'role']:
            session.pop(key, None)
        return redirect(url_for('auth.login'))
        
    @auth_bp.route('/api/register', methods=['POST'])
    def api_register():
        data = request.json
        success, message = auth_service.register(data['username'], data['password'], data.get('role', 'customer'))
        return jsonify({'success': success, 'message': message})

    @auth_bp.route('/api/login', methods=['POST'])
    def api_login():
        data = request.json
        user = auth_service.login(data['username'], data['password'])
        return jsonify({'success': bool(user), 'user': user})

    return auth_bp
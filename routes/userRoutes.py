from flask import Blueprint, render_template, request, redirect, url_for
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if db.session.query(User).filter_by(username=username).first(): # Ubah cara query
            return render_template('register.html', error='Username sudah terdaftar.')
        if db.session.query(User).filter_by(email=email).first(): # Ubah cara query
            return render_template('register.html', error='Email sudah terdaftar.')

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            return 'Login berhasil!' # Ganti dengan redirect ke halaman utama
        else:
            return render_template('login.html', error='Username atau password salah.')
    return render_template('login.html')

@auth_bp.route('/')
def index():
    return redirect(url_for('auth.login'))
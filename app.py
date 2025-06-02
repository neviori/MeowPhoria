from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, session
import os
from flask_sqlalchemy import SQLAlchemy
from app.services.matchService import calculate_breed_score

db = SQLAlchemy()

app = Flask(__name__,
            static_folder='app/static',
            template_folder='app/templates')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'meow_secret_key')

from app.routes import main
app.register_blueprint(main)

from routes.whiskermatchRoutes import whiskermatch_bp
app.register_blueprint(whiskermatch_bp)

# Penyimpanan user sementara (dummy)
users = {}

# Home page
# @app.route('/home')
# def home():
#     return render_template('home.html')

# Halaman utama
@app.route('/')
def index():
    return render_template('home.html')

# Login dummy (admin only)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'admin':
            session['user'] = 'admin'
            return redirect(url_for('main.home'))
    return render_template('login.html')

# Login user terdaftar
@app.route('/auth/login', methods=['GET', 'POST'])
def auth_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('index'))
        flash('Username atau password salah, meow! 😿', 'error')
    return render_template('home.html')

# Register user baru
@app.route('/auth/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if len(username) < 3 or len(password) < 6:
            flash('Username atau password tidak memenuhi syarat, meow!', 'error')
        elif username in users:
            flash('Username sudah digunakan, meow!', 'error')
        else:
            users[username] = password
            flash('Akun berhasil dibuat! Silakan login ya, meow 😸', 'info')
            return redirect(url_for('auth_login'))
    return render_template('register.html')

# Whisker Match page
@app.route('/whiskermatch', methods=['GET', 'POST'])
def whisker_match():
    if request.method == 'GET':
        answers = request.get_json()
        if not answers:
            return jsonify({"error": "Tidak ada data jawaban"}), 400

        best_match, scores = calculate_breed_score(answers)
        return jsonify({
            "best_match": best_match,
            "scores": scores
        })
    return render_template('whiskermatch.html')


# Logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

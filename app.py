from flask import Flask, render_template, request, redirect, url_for, flash, session
from app.routes import main  # pastikan blueprint `main` ada
import os

app = Flask(__name__,
            static_folder='app/static',
            template_folder='app/templates')
app.secret_key = os.environ.get('SECRET_KEY', 'meow_secret_key')
app.register_blueprint(main)

# Penyimpanan user sementara (dummy)
users = {}

# Home page
@app.route('/home')
def home():
    return render_template('home.html')

# Halaman utama
@app.route('/')
def index():
     if 'username' in session:
         return render_template('home.html')
     return redirect(url_for('auth_login'))

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
    return render_template('login.html')

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
#whisker match 
@app.route('/WhiskerMatch')
@app.route('/whiskermatch')
def whisker_match():
    return render_template('whiskermatch.html')

@app.route('/perawatan')
def perawatan():
    return render_template('perawatan.html')
@app.route('/booking')
def booking():
    return render_template('booking.html')

# Logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

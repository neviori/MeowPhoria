from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, session
import os
from flask_sqlalchemy import SQLAlchemy
from app.services.matchService import calculate_breed_score
from models import db, Service, Package
from perawatanroutes import perawatan_bp

db = SQLAlchemy()

app = Flask(__name__,
            static_folder='app/static',
            template_folder='app/templates')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///perawatan_kucing.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'meow_secret_key')

def initialize_data(app):
    """Fungsi untuk menginisialisasi data awal jika belum ada."""
    with app.app_context():
        
        if not Service.query.first():
            print("Database kosong atau belum terisi. Memulai inisialisasi data...")
            db.drop_all() 
            db.create_all()

            # Tambahkan Layanan
            grooming_service = Service(name='Grooming')
            vaksin_service = Service(name='Vaksin')
            penitipan_service = Service(name='Penitipan')

            db.session.add_all([grooming_service, vaksin_service, penitipan_service])
            db.session.commit()
            print("Layanan ditambahkan.")

            # Tambahkan Paket Grooming
            db.session.add_all([
                Package(service=grooming_service, name='Paket Basic', price=50000.0,
                        description='Mandi Kucing, Pengeringan & Penyisiran Bulu, Pembersihan Telinga, Pemotongan Kuku'),
                Package(service=grooming_service, name='Paket Premium', price=100000.0,
                        description='Semua Layanan Paket Basic, Pembersihan Kelenjar Anal, Pemberian Parfum Khusus, Anti Kutu, Potong Bulu'),
                Package(service=grooming_service, name='Paket Styling', price=170000.0,
                        description='Semua Layanan Paket Premium, Potong Bulu Model, Styling Ekor/Telinga, Aksesoris (Bandana/Ribbon), Foto After Grooming')
            ])
            db.session.commit()
            print("Paket Grooming ditambahkan.")

            # Tambahkan Paket Vaksin
            db.session.add_all([
                Package(service=vaksin_service, name='Vaksin Colostrum', price=80000.0,
                        description='Fungsi: Memberi antibodi awal lewat kolostrum; Usia: Baru lahir sampai 4 minggu'),
                Package(service=vaksin_service, name='Vaksin Neonatal', price=100000.0,
                        description='Fungsi: Vaksin untuk anak kucing sangat muda; Usia: 4–6 minggu'),
                Package(service=vaksin_service, name='Vaksin Tricat', price=150000.0,
                        description='Fungsi: Melindungi dari Panleukopenia, Calicivirus, Rhinotracheitis; Usia: 8 minggu'),
                Package(service=vaksin_service, name='Vaksin Tetracat', price=200000.0,
                        description='Fungsi: Tricat + perlindungan terhadap Chlamydia; Usia: 12 minggu ke atas'),
                Package(service=vaksin_service, name='Vaksin Rabies', price=100000.0,
                        description='Fungsi: Pencegahan penyakit rabies; Usia: Minimal 12 minggu')
            ])
            db.session.commit()
            print("Paket Vaksin ditambahkan.")

            # Tambahkan Paket Penitipan
            db.session.add_all([
                Package(service=penitipan_service, name='Penitipan Harian', price=40000.0,
                        description='Kandang bersih & nyaman, Makan 2x sehari (bisa bawa sendiri), Pembersihan litter box, Update foto/video via WhatsApp'),
                Package(service=penitipan_service, name='Penitipan Mingguan', price=250000.0,
                        description='Semua layanan Paket Harian, Grooming ringan 1x, Bermain & interaksi harian, Update harian via WhatsApp'),
                Package(service=penitipan_service, name='Penitipan Bulanan', price=900000.0,
                        description='Semua layanan Paket Mingguan, Grooming mingguan, Pemantauan kesehatan dasar, Laporan & foto/video berkala via WhatsApp')
            ])
            db.session.commit()
            print("Paket Penitipan ditambahkan.")
            print("Database berhasil diinisialisasi dengan data sampel.")
        else:
            print("Database sudah berisi data. Melewatkan inisialisasi data.")

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

@app.route('/ajukan_adopsi')
def ajukan_adopsi():
    nama_kucing = request.args.get('nama_kucing')

    # contoh data dummy, bisa juga diimpor dari file
    kucing_dict = {
        "Luna": {
            "usia": "26 bulan",
            "ras": "Persia",
            "deskripsi": "Kucing manja dan suka dipeluk. Cocok untuk keluarga dengan anak-anak."
        },
        "Milo": {
            "usia": "18 bulan",
            "ras": "Anggora",
            "deskripsi": "Aktif dan suka bermain. Membutuhkan ruang luas untuk eksplorasi."
        },
        "Leo": {
            "usia": "20 bulan",
            "ras": "Maine Coon",
            "deskripsi": "Tenang dan penyayang. Sering tidur siang dan senang disisir bulunya."
        },
        "Bella": {
            "usia": "13 bulan",
            "ras": "Ragdoll",
            "deskripsi": "Ceria dan lincah. Sangat ramah dengan manusia maupun hewan lain."
        }
    }

    data = kucing_dict.get(nama_kucing)

    if not data:
        return "Kucing tidak ditemukan", 404

    kucing_data = {
        "nama": nama_kucing,
        "usia": data["usia"],
        "ras": data["ras"],
        "deskripsi": data["deskripsi"]
    }

    return render_template("konfirmasi.html", kucing=kucing_data)


@app.route('/konfirmasi-adopsi', methods=['POST'])
def konfirmasi_adopsi():
    nama_kucing = request.form.get('nama_kucing')
    nama_pengadopsi = request.form.get('nama_pengadopsi')
    alamat_pengadopsi = request.form.get('alamat_pengadopsi')
    kontak_pengadopsi = request.form.get('kontak_pengadopsi')
    print(f"Pengajuan adopsi untuk {nama_kucing} oleh {nama_pengadopsi}")
    print(f"Alamat: {alamat_pengadopsi}, Kontak: {kontak_pengadopsi}")

    flash(f'Pengajuan adopsi untuk {nama_kucing} berhasil diajukan!', 'success')
    return redirect(url_for('index'))

# Logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        initialize_data(app)
    app.run(debug=True)
# if __name__ == '__main__':
#     app.run(debug=True)

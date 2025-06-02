from flask import Flask, render_template, request, redirect, url_for, flash, session
import os

app = Flask(__name__,
            static_folder='app/static',
            template_folder='app/templates')
app.secret_key = os.environ.get('SECRET_KEY', 'meow_secret_key')

# Penyimpanan user sementara (dummy)
users = {}

# Halaman utama
@app.route('/') 
def index():
    # if 'username' in session:
        return render_template('home.html')
    # return redirect(url_for('main.home'))

# Login dummy (admin only)
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         if request.form['username'] == 'admin' and request.form['password'] == 'admin':
#             session['user'] = 'admin'
#             return redirect(url_for('main.home'))
#     return render_template('login.html')

# # Login user terdaftar
# @app.route('/auth/login', methods=['GET', 'POST'])
# def auth_login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         if username in users and users[username] == password:
#             session['username'] = username
#             return redirect(url_for('index'))
#         flash('Username atau password salah, meow! 😿', 'error')
#     return render_template('login.html')

# # Register user baru
# @app.route('/auth/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         if len(username) < 3 or len(password) < 6:
#             flash('Username atau password tidak memenuhi syarat, meow!', 'error')
#         elif username in users:
#             flash('Username sudah digunakan, meow!', 'error')
#         else:
#             users[username] = password
#             flash('Akun berhasil dibuat! Silakan login ya, meow 😸', 'info')
#             return redirect(url_for('auth_login'))
#     return render_template('register.html')

# Logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('user', None)
    return redirect(url_for('login'))

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
# Jalankan aplikasi
if __name__ == '__main__':
    app.run(debug=True)

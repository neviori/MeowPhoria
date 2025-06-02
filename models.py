from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    

class WhiskerMatch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    personality_description = db.Column(db.String(250), nullable=True)
    image_filename = db.Column(db.String(100), nullable=True) # misal: 'milo.png'

    environment_preference = db.Column(db.String(50))  # Lingkungan tempat tinggal
    play_time_needed = db.Column(db.String(50))       # Waktu luang untuk bermain
    owner_experience = db.Column(db.String(50))       # Pengalaman merawat
    social_compatibility = db.Column(db.String(50))   # Anak kecil/hewan lain
    cat_personality_type = db.Column(db.String(50))

    
# class Cat(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80), unique=True, nullable=False)
#     personality_description = db.Column(db.String(250), nullable=True)
#     image_filename = db.Column(db.String(100), nullable=True) # misal: 'milo.png'

#     environment_preference = db.Column(db.String(50))  # Lingkungan tempat tinggal
#     play_time_needed = db.Column(db.String(50))       # Waktu luang untuk bermain
#     owner_experience = db.Column(db.String(50))       # Pengalaman merawat
#     social_compatibility = db.Column(db.String(50))   # Anak kecil/hewan lain
#     cat_personality_type = db.Column(db.String(50))   # Apa yang dicari dari kucing

#     def __repr__(self):
#         return f'<Cat {self.name}>'

# (Opsional) Fungsi untuk mengisi data awal kucing jika database kosong
# def populate_initial_cats():
#     if Cat.query.count() == 0:
#         cats_data = [
#             {"name": "Milo", "personality_description": "Aktif dan suka bermain, cocok untuk rumah yang ramai.", "image_filename": "milo.png", "environment_preference": "Ramai", "play_time_needed": "Banyak", "owner_experience": "Punya", "social_compatibility": "Ada", "cat_personality_type": "Teman Aktif"},
#             {"name": "Luna", "personality_description": "Tenang dan penyayang, teman sempurna untuk bersantai.", "image_filename": "luna.png", "environment_preference": "Tenang", "play_time_needed": "Sedikit", "owner_experience": "Belum", "social_compatibility": "Tidak Ada", "cat_personality_type": "Sahabat Tenang"},
#             {"name": "Simba", "personality_description": "Pemberani dan penasaran, selalu siap untuk petualangan baru.", "image_filename": "simba.png", "environment_preference": "Ramai", "play_time_needed": "Banyak", "owner_experience": "Punya", "social_compatibility": "Ada", "cat_personality_type": "Teman Aktif"},
#             {"name": "Nala", "personality_description": "Manis dan lembut, sangat cocok untuk pemilik pertama kali.", "image_filename": "nala.png", "environment_preference": "Tenang", "play_time_needed": "Sedikit", "owner_experience": "Belum", "social_compatibility": "Tidak Ada", "cat_personality_type": "Sahabat Tenang"},
#             # Tambahkan data kucing lainnya di sini
#             # Pastikan Anda memiliki gambar 'milo.png', 'luna.png', dll. di static/img/
#         ]
#         for cat_info in cats_data:
#             cat = Cat(**cat_info)
#             db.session.add(cat)
#         db.session.commit()
#         print("Data kucing awal telah ditambahkan ke database.")
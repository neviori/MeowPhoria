from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from datetime import datetime

db = SQLAlchemy()

class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    cat_name = db.Column(db.String(100), nullable=False)
    cat_breed = db.Column(db.String(100), nullable=False)
    cat_age = db.Column(db.Float, nullable=False)
    booking_date = db.Column(db.Date, nullable=False)
    queue_number = db.Column(db.Integer, nullable=False)
    booking_timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    services_booked = db.relationship('BookingService', back_populates='booking', cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'customer_name': self.customer_name,
            'cat_name': self.cat_name,
            'cat_breed': self.cat_breed,
            'cat_age': self.cat_age,
            'booking_date': self.booking_date.isoformat(),
            'queue_number': self.queue_number,
            'booking_timestamp': self.booking_timestamp.isoformat(),
            'services_booked': [bs.to_dict() for bs in self.services_booked]
        }

class Service(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    packages = db.relationship('Package', backref='service', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }

class Package(db.Model):
    __tablename__ = 'packages'
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'service_id': self.service_id,
            'name': self.name,
            'price': self.price,
            'description': self.description
        }

class BookingService(db.Model):
    __tablename__ = 'bookingaku udah ngisi_services'
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), primary_key=True)
    package_id = db.Column(db.Integer, db.ForeignKey('packages.id'), primary_key=True)
    duration_value = db.Column(db.Integer, nullable=True)
    duration_unit = db.Column(db.String(20), nullable=True)

    booking = db.relationship('Booking', back_populates='services_booked')
    package = db.relationship('Package')

    def to_dict(self):
        package_info = self.package.to_dict()
        booking_service_data = {
            'service_name': self.package.service.name,
            'package_name': package_info['name'],
            'price': package_info['price']
        }
        if self.duration_value is not None and self.duration_unit:
            booking_service_data['duration'] = f"{self.duration_value} {self.duration_unit}"
        return booking_service_data
      
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    

class WhiskerMatch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    personality_description = db.Column(db.String(250), nullable=True)
    image_filename = db.Column(db.String(100), nullable=True) 

    environment_preference = db.Column(db.String(50)) 
    play_time_needed = db.Column(db.String(50))    
    owner_experience = db.Column(db.String(50))    
    social_compatibility = db.Column(db.String(50))   
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

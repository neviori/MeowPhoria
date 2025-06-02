from flask import Flask
from models import db, Service, Package
from perawatanroutes import perawatan_bp

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///perawatan_kucing.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    app.register_blueprint(perawatan_bp, url_prefix='/api')
    return app

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


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
        initialize_data(app)
    app.run(debug=True)
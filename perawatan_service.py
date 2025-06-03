from models import db, Booking, Service, Package, BookingService
from datetime import datetime, date
from sqlalchemy import func

class PerawatanService:
    @staticmethod
    def get_all_services():
        """Mengambil semua layanan yang tersedia."""
        services = Service.query.all()
        return [s.to_dict() for s in services]

    @staticmethod
    def get_packages_by_service_name(service_name):
        """Mengambil paket berdasarkan nama layanan."""
        service = Service.query.filter_by(name=service_name).first()
        if not service:
            return None
        packages = Package.query.filter_by(service_id=service.id).all()
        return [p.to_dict() for p in packages]

    @staticmethod
    def get_package_by_id(package_id):
        """Mengambil detail paket berdasarkan ID."""
        package = Package.query.get(package_id)
        return package.to_dict() if package else None

    @staticmethod
    def create_booking(customer_name, cat_name, cat_breed, cat_age, booking_date_str, services_data):
        """Membuat booking baru."""
        try:
            booking_date = datetime.strptime(booking_date_str, '%Y-%m-%d').date()
        except ValueError:
            raise ValueError("Format tanggal booking tidak valid. Gunakan YYYY-MM-DD.")
        
        max_queue = db.session.query(func.max(Booking.queue_number)).filter_by(booking_date=booking_date).scalar()
        queue_number = (max_queue or 0) + 1

        new_booking = Booking(
            customer_name=customer_name,
            cat_name=cat_name,
            cat_breed=cat_breed,
            cat_age=cat_age,
            booking_date=booking_date,
            queue_number=queue_number
        )
        db.session.add(new_booking)
        db.session.flush()

        for service_info in services_data:
            package_id = service_info.get('package_id')
            duration_value = service_info.get('duration_value')
            duration_unit = service_info.get('duration_unit')

            package = Package.query.get(package_id)
            if not package:
                db.session.rollback()
                raise ValueError(f"Paket dengan ID {package_id} tidak ditemukan.")

            if package.service.name == 'Penitipan':
                if not (duration_value and duration_unit):
                    db.session.rollback()
                    raise ValueError("Nilai dan unit durasi wajib untuk paket penitipan.")
                if duration_value <= 0:
                    db.session.rollback()
                    raise ValueError("Durasi penitipan harus lebih dari 0.")
            else:
                if duration_value is not None or duration_unit is not None:
                    db.session.rollback()
                    raise ValueError(f"Durasi tidak diperlukan untuk layanan {package.service.name}.")

            booking_service = BookingService(
                booking=new_booking,
                package=package,
                duration_value=duration_value,
                duration_unit=duration_unit
            )
            db.session.add(booking_service)

        db.session.commit()
        return new_booking.to_dict()

    @staticmethod
    def get_all_bookings():
        """Mengambil semua booking, diurutkan berdasarkan tanggal dan nomor antrian."""
        bookings = Booking.query.order_by(Booking.booking_date.asc(), Booking.queue_number.asc()).all()
        return [b.to_dict() for b in bookings]

    @staticmethod
    def get_booking_by_id(booking_id):
        """Mengambil detail booking berdasarkan ID."""
        booking = Booking.query.get(booking_id)
        return booking.to_dict() if booking else None
    
    @staticmethod
    def get_antrian_by_tanggal(tanggal_str):
        """
        Mengambil daftar antrian berdasarkan tanggal booking.
        """
        try:
            tanggal = datetime.strptime(tanggal_str, '%Y-%m-%d').date()
        except ValueError:
            raise ValueError("Format tanggal tidak valid. Gunakan YYYY-MM-DD.")

        bookings = Booking.query \
            .filter_by(booking_date=tanggal) \
            .order_by(Booking.queue_number.asc()) \
            .all()
        
        hasil = []  
        for b in bookings:
            layanan_list = []
            paket_list = []

            for bs in b.booking_services:  
                layanan_list.append(bs.package.service.name)
                paket_list.append(bs.package.name)

            hasil.append({
                "nama_customer": b.customer_name,
                "nama_kucing": b.cat_name,
                "layanan": layanan_list,
                "paket": paket_list,
                "nomor_antrian": b.queue_number
            })

        return hasil 
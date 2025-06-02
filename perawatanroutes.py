from flask import Blueprint, request, jsonify
from perawatan_service import PerawatanService
from datetime import datetime

#Blueprint utama
perawatan_bp = Blueprint('perawatan_bp', __name__)

# ==================== SERVICE ROUTES ====================
@perawatan_bp.route('/services', methods=['GET'])
def get_services():
    """Endpoint untuk mendapatkan semua jenis layanan."""
    services = PerawatanService.get_all_services()
    return jsonify(services), 200

@perawatan_bp.route('/services/<string:service_name>/packages', methods=['GET'])
def get_packages_for_service(service_name):
    """Endpoint untuk mendapatkan paket berdasarkan nama layanan (misal: 'Grooming')."""
    packages = PerawatanService.get_packages_by_service_name(service_name)
    if packages is None:
        return jsonify({"message": f"Layanan '{service_name}' tidak ditemukan."}), 404
    return jsonify(packages), 200

# ==================== BOOKING ROUTES ====================
@perawatan_bp.route('/bookings', methods=['POST'])
def create_booking():
    """Endpoint untuk membuat booking baru."""
    data = request.get_json()
    if not data:
        return jsonify({"message": "Data JSON tidak valid."}), 400

    required_fields = ['customer_name', 'cat_name', 'cat_breed', 'cat_age', 'booking_date', 'services']
    for field in required_fields:
        if field not in data:
            return jsonify({"message": f"Field wajib '{field}' tidak ada."}), 400
    
    if not isinstance(data['services'], list) or not data['services']:
        return jsonify({"message": "Daftar layanan tidak valid atau kosong."}), 400

    try:
        new_booking = PerawatanService.create_booking(
            data['customer_name'],
            data['cat_name'],
            data['cat_breed'],
            data['cat_age'],
            data['booking_date'],
            data['services']
        )
        return jsonify(new_booking), 201
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        print(f"Error saat membuat booking: {e}")
        return jsonify({"message": "Terjadi kesalahan saat membuat booking.", "error": str(e)}), 500

@perawatan_bp.route('/bookings', methods=['GET'])
def get_all_bookings():
    """Endpoint untuk mendapatkan semua booking yang sudah ada."""
    bookings = PerawatanService.get_all_bookings()
    return jsonify(bookings), 200

@perawatan_bp.route('/bookings/<int:booking_id>', methods=['GET'])
def get_booking_details(booking_id):
    """Endpoint untuk mendapatkan detail booking berdasarkan ID."""
    booking = PerawatanService.get_booking_by_id(booking_id)
    if not booking:
        return jsonify({"message": "Booking tidak ditemukan."}), 404
    return jsonify(booking), 200

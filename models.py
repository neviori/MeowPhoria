from flask_sqlalchemy import SQLAlchemy
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
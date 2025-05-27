from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from models import db
from routes.userRoutes import auth_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' # atau konfigurasi database lainnya
db.init_app(app)

app.register_blueprint(auth_bp)

@app.route("/")
def login():
    return render_template('login.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
from flask import Blueprint, render_template

main = Blueprint("main", __name__)

@main.route('/')
def home_page():
    return render_template('home.html')

@main.route("/Perawatan")
def gallery():
    return render_template("perawatan.html")

@main.route("/booking")
def about():
    return render_template("booking.html")

@main.route("/adopsi")
def adopt():
    return render_template("adopsi.html")

@main.route("/konfirmasi")
def adopt():
    return render_template("konfirmasi.html")

@main.route("/whishkermatch")
def whiskermatch():
    return render_template("whiskermatch.html")
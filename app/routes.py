from flask import Blueprint, render_template

main = Blueprint("main", __name__)

@main.route('/home')
def home():
    return render_template('home.html')

@main.route("/gallery")
def gallery():
    return render_template("gallery.html")

@main.route("/about")
def about():
    return render_template("about.html")

@main.route("/adopt")
def adopt():
    return render_template("adopt.html")
@main.route("/konfirmasi")
def adopt():
    return render_template("konfirmasi.html")

@main.route("/")
def whiskermatch():
    return render_template("whiskermatch.html")
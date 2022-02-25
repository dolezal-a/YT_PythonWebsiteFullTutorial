from flask import Blueprint, render_template, request, flash, url_for, redirect
from website import views
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

auth = Blueprint("auth", __name__)


@auth.route("/login")
def login():
    return render_template("login.html")


@auth.route("/logout")
def logout():
    return "<p>Logout</p>"


@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        firstName = request.form.get("firstName")
        lastName = request.form.get("lastName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        if len(email) < 4:
            flash("Email must be grater than 4 characters.", category="error")
        elif len(firstName) < 2:
            flash("Fist Name must be grater than 2 characters.", category="error")
        elif password1 != password2:
            flash("Password don't match.", category="error")
        elif len(password1) < 7:
            flash("Password must be at least 7 characters.", category="error")
        else:
            new_user = User(email=email, first_name = firstName, last_name=lastName, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()

            flash("Account created.", category="success")
            return redirect(url_for('views.home'))

    return render_template("sign_up.html")

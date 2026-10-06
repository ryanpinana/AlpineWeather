from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

from flask_login import login_user
from flask_login import logout_user

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from models.conn import db
from models.user import User


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        existing_user = User.query.filter(
            (User.username == username)
            | (User.email == email)
        ).first()

        if existing_user:
            return "Utente già esistente"

        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )

        db.session.add(user)
        db.session.commit()

        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():


    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(
            username=username
        ).first()

        if user and check_password_hash(
            user.password_hash,
            password
        ):

            login_user(user)

            return redirect(url_for("weather.weather"))

        return render_template("login.html", hasError=True)

    return render_template("login.html", hasError=False)


@auth_bp.route("/logout")
def logout():

    logout_user()

    return redirect(
        url_for("auth.login")
    )
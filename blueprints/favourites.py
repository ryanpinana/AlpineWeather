from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

from models.conn import db
from models.favourite_city import FavoriteCity

favourites_bp = Blueprint(
    "favourites",
    __name__,
    url_prefix="/favourites"
)

@favourites_bp.route("/")
@login_required
def favourites():
    cities = FavoriteCity.query.filter_by(
        user_id=current_user.id
    ).all()

    return render_template("favourites.html", cities=cities)

@favourites_bp.route("/add/<city>")
@login_required
def add_favourite(city):
    existing = FavoriteCity.query.filter_by(
        city_name=city,
        user_id=current_user.id
    ).first()

    if not existing:
        favourite = FavoriteCity(
            city_name=city,
            user_id=current_user.id
        )

        db.session.add(favourite)
        db.session.commit()

    return redirect(url_for("favourites.favourites"))

@favourites_bp.route("/delete/<int:id>")
@login_required
def delete_favourite(id):
    city = FavoriteCity.query.filter_by(
        id=id,
        user_id=current_user.id
    ).first()

    if city:
        db.session.delete(city)
        db.session.commit()

    return redirect(url_for("favourites.favourites"))


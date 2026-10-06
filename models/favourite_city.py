from models.conn import db


class FavoriteCity(db.Model):
    __tablename__ = "favorite_cities"

    id = db.Column(db.Integer, primary_key=True)

    city_name = db.Column(
        db.String(100),
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )
from flask import Flask

from flask_login import LoginManager

from models.conn import db


login_manager = LoginManager()


def create_app():

    app = Flask(__name__)

    # Configurazione
    app.config["SECRET_KEY"] = "super-secret-key"

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "sqlite:///sqlalchemy_app.db"
    )

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Inizializzazione database
    db.init_app(app)

    # Inizializzazione Flask-Login
    login_manager.init_app(app)

    login_manager.login_view = "auth.login"

    # Import del modello User
    from models.user import User

    @login_manager.user_loader
    def load_user(user_id):

        return User.query.get(int(user_id))

    # Registrazione Blueprint
    from blueprints.auth import auth_bp
    from blueprints.weather import weather_bp
    from blueprints.favourites import favourites_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(weather_bp)
    app.register_blueprint(favourites_bp)

    # Creazione delle tabelle
    with app.app_context():

        db.create_all()

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
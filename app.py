import os

from flask import Flask

from flask_login import LoginManager

from models.conn import db

from dotenv import load_dotenv

load_dotenv()


login_manager = LoginManager()


def create_app(test_config=None):

    app = Flask(__name__)

    # Configurazione
    app.config["SECRET_KEY"] = os.getenv('SECRET_KEY')

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if test_config:
        app.config.update(test_config)

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
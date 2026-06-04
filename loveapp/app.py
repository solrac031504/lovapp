import os

from dotenv import load_dotenv
from extensions import db, login_manager
from flask import Flask


def create_app() -> Flask:
    app = Flask(__name__)

    # Load .env
    load_dotenv()

    # Grab values
    secret_key: str | None = os.getenv("SECRET_KEY")
    sqlalchemy_database_uri: str | None = os.getenv("SQLALCHEMY_DATABASE_URI")

    # Ensure values are present
    if not secret_key:
        raise ValueError("SECRET_KEY cannot be null")
    if not sqlalchemy_database_uri:
        raise ValueError("SQLALCHEMY_DATABASE_URI cannot be null")

    app.config["SECRET_KEY"] = secret_key
    app.config["SQLALCHEMY_DATABASE_URI"] = sqlalchemy_database_uri

    db.init_app(app)
    login_manager.init_app(app)

    # Register blueprints

    # Create all tables on first run
    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    create_app().run(debug=True)

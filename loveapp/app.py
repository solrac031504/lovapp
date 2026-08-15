import os
import secrets

from dotenv import load_dotenv
from flask import Flask

if __package__:
    from . import models
    from .extensions import db, login_manager
else:
    import models  # noqa: F401
    from extensions import db, login_manager


def create_app() -> Flask:
    app = Flask(__name__, instance_relative_config=True)

    # Load .env from the app directory so the database URI is stable
    load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

    # Use the configured secret or a generated fallback.
    secret_key: str = os.getenv("SECRET_KEY") or secrets.token_hex()
    default_db_path: str = os.path.join(app.instance_path, "LoveApp.db")
    sqlalchemy_database_uri: str = os.getenv(
        "SQLALCHEMY_DATABASE_URI", f"sqlite:///{default_db_path}"
    )
    if sqlalchemy_database_uri.startswith("sqlite:///"):
        sqlite_path: str = sqlalchemy_database_uri.replace("sqlite:///", "", 1)
        if not os.path.isabs(sqlite_path):
            sqlite_path: str = os.path.abspath(
                os.path.join(os.path.dirname(__file__), sqlite_path)
            )
            sqlalchemy_database_uri = f"sqlite:///{sqlite_path}"

    app.config["SECRET_KEY"] = secret_key
    app.config["SQLALCHEMY_DATABASE_URI"] = sqlalchemy_database_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    login_manager.init_app(app)

    # Register blueprints

    @app.route("/")
    def home() -> str:
        return "Hello world"

    # Create all tables on first run
    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    create_app().run(debug=True)

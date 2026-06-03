from extensions import db, login_manager
from flask import Flask


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "placeholder"
    app.config["SQLALCHEMY_DATABASE_URI"] = "placeholder"

    db.init_app(app)
    login_manager.init_app(app)

    # Register blueprints

    # Create all tables on first run
    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    create_app().run(debug=True)

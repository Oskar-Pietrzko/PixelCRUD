from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db: SQLAlchemy = SQLAlchemy()

def create_app() -> Flask:
    app: Flask = Flask(__name__)
    app.config.from_object("config.Config")
    app.json.sort_keys = False

    db.init_app(app)

    with app.app_context():
        from app.controllers import register_routes

        register_routes(app)

        db.create_all()

    return app

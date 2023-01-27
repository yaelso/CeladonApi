from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_cors import CORS
import os

db = SQLAlchemy()
migrate = Migrate()
load_dotenv()


def create_app(test_config=None):
    app = Flask(__name__)

    if not test_config:
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")

    else:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_TEST_DATABASE_URI")

    from app.models.category import Category
    from app.models.checklist import Checklist
    from app.models.checklist_status import Checklist_Status
    from app.models.task import Task
    from app.models.pokemon import Pokemon
    from app.models.user import User

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes.category_routes import categories_bp
    app.register_blueprint(categories_bp)

    CORS(app)
    return app

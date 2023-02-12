import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_cors import CORS
from flask_firebase_admin import FirebaseAdmin
from firebase_admin import credentials
import os

db = SQLAlchemy()
migrate = Migrate()
firebase = FirebaseAdmin()

load_dotenv()


def create_app(test_config=None):
    app = Flask(__name__)

    # cert = {
    #     "type": os.environ.get("CELADON_FIREBASE_TYPE"),
    #     "project_id": os.environ.get("CELADON_FIREBASE_PROJECT_ID"),
    #     "private_key_id": os.environ.get("CELADON_FIREBASE_PRIVATE_KEY_ID"),
    #     "private_key": os.environ.get("CELADON_FIREBASE_PRIVATE_KEY"),
    #     "client_email": os.environ.get("CELADON_FIREBASE_CLIENT_EMAIL"),
    #     "client_id": os.environ.get("CELADON_FIREBASE_CLIENT_ID"),
    #     "auth_uri": os.environ.get("CELADON_FIREBASE_AUTH_URI"),
    #     "token_uri": os.environ.get("CELADON_FIREBASE_TOKEN_URI"),
    #     "auth_provider_x509_cert_url": os.environ.get("CELADON_FIREBASE_AUTH_PROVIDER_X509_CERT_URL"),
    #     "client_x509_cert_url": os.environ.get("CELADON_FIREBASE_AUTH_CLIENT_X509_CERT_URL")
    # }

    cert = json.loads(os.environ.get("SERVICE_ACCOUNT"))

    app.config["FIREBASE_ADMIN_CREDENTIAL"] = credentials.Certificate(cert)
    firebase.init_app(app)

    if not test_config:
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")

    else:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_TEST_DATABASE_URI")

    from app.models.category import Category
    from app.models.checklist import Checklist
    from app.models.task import Task
    from app.models.habit import Habit
    from app.models.pokemon import Pokemon
    from app.models.user_pokemon import UserPokemon
    from app.models.user import User

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes.category_routes import categories_bp
    app.register_blueprint(categories_bp)

    from app.routes.checklist_routes import checklists_bp
    app.register_blueprint(checklists_bp)

    from app.routes.task_routes import tasks_bp
    app.register_blueprint(tasks_bp)

    from app.routes.habit_routes import habits_bp
    app.register_blueprint(habits_bp)

    from app.routes.pokemon_routes import pokemon_bp
    app.register_blueprint(pokemon_bp)

    from app.routes.user_pokemon_routes import user_pokemon_bp
    app.register_blueprint(user_pokemon_bp)

    from app.routes.user_routes import users_bp
    app.register_blueprint(users_bp)

    CORS(app)
    return app

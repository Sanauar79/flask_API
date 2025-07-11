from flask import Flask
from .extensions import db, mail, bcrypt, migrate
from .config import Config
from .routes.auth import auth_bp
from .routes.contact import contact_bp
from .routes.admin import admin_bp
from app.routes.user import messages_bp
from dotenv import load_dotenv

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    mail.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    load_dotenv()

    app.register_blueprint(auth_bp)
    app.register_blueprint(contact_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(messages_bp)

    return app

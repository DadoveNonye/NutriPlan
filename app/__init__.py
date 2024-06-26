from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_login import LoginManager


db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    login_manager.init_app(app)
    
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp)


    

    return app


from app import models

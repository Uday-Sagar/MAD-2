from datetime import timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from website.celery_config import make_celery
from flask_jwt_extended import JWTManager   

db=SQLAlchemy()
mail = Mail()
celery = None
jwt = JWTManager()

def create_app():
    global celery
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
    app.config["SECRET_KEY"] = "secret_key"  

    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'admin@homicare.com'
    app.config['MAIL_PASSWORD'] = 'jus20029@'

    app.config["JWT_SECRET_KEY"] = "secret_key"
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]  # ✅ Ensure JWT is stored in cookies
    app.config["JWT_COOKIE_SECURE"] = False  # ❌ Set to True in production (HTTPS only)
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1) 

    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    celery = make_celery(app)

    from website.auth import auth
    from website.routes import views
    from website.admin_routes import admin
    from website.customers_routes import cust
    from website.service_professionals_routes import prof
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(admin,url_prefix='/')
    app.register_blueprint(cust,url_prefix='/')
    app.register_blueprint(prof,url_prefix='/')
    
    
    create_database(app)

    return app

def create_database(app):
    with app.app_context():
        db.create_all()
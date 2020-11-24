from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import find_modules, import_string 
from flask_login import LoginManager
from flask_httpauth import HTTPBasicAuth
from flask_bcrypt import Bcrypt
from flask_mail import Mail

db = SQLAlchemy()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message_category = 'info'
httpauth = HTTPBasicAuth()
bcrypt = Bcrypt()
mail = Mail()

def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(config_class)

	db.init_app(app)
	login.init_app(app)
	bcrypt.init_app(app)
	mail.init_app(app)

	from app.blueprints.api.routes import api
	app.register_blueprint(api)

	from app.blueprints.main.routes import main
	app.register_blueprint(main)

	from app.blueprints.auth.routes import auth
	app.register_blueprint(auth)

	return app
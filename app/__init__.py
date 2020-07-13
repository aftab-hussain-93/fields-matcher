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
	app.config.from_object(Config)
	db.init_app(app)
	login.init_app(app)
	bcrypt.init_app(app)
	mail.init_app(app)
	from app.blueprints.api.routes import api
	from app.blueprints.main.routes import main
	from app.blueprints.auth.routes import auth
	from app.blueprints.test.routes import test
	app.register_blueprint(api)
	app.register_blueprint(main)
	app.register_blueprint(auth)
	app.register_blueprint(test)
	with app.app_context():
		db.create_all()
	return app

# def register_blueprints(app):
# 	for name in find_modules('app.blueprints', include_packages=True,recursive=True):
# 		print(name)
# 		mod = import_string(name,silent=True)
# 		if hasattr(mod, 'Blueprint'):
# 			print(f"Register {mod}")
# 			app.register_blueprint(mod.Blueprint)
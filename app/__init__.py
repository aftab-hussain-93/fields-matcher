from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import find_modules, import_string 

db = SQLAlchemy()


def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(Config)
	db.init_app(app)
	from app.blueprints.api.routes import api
	from app.blueprints.main.routes import main
	app.register_blueprint(api)
	app.register_blueprint(main)
	return app

def register_blueprints(app):
	for name in find_modules('app.blueprints'):
		print(name)
		mod = import_string(name)
		if hasattr(mod, 'blueprint'):
			print(f"Register {mod}")
			app.register_blueprint(mod.blueprint)
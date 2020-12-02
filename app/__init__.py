from flask import Flask
from app.config import Config
from .extensions import mongo, login

def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(config_class)

	mongo.init_app(app)

	# login.init_app(app)
	# bcrypt.init_app(app)
	# mail.init_app(app)

	# from app.blueprints.api.routes import api
	# app.register_blueprint(api)

	from app.blueprints.main.views import main
	app.register_blueprint(main)

	# from app.blueprints.auth.routes import auth
	# app.register_blueprint(auth)

	return app
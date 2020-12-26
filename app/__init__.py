from flask import Flask
from app.config import Config
from .extensions import mongo, login_manager, bcrypt
import logging, os
from pathlib import Path

def create_app(config_class=Config):
	static_path = Path.cwd().joinpath('ui','static')
	static_p = os.path.join(os.path.dirname(os.getcwd()), r'ui/static')
	app = Flask(__name__, static_folder=static_p)
	app.config.from_object(config_class)
	
	#logging.basicConfig(filename='error.log',level=logging.INFO)

#	app.static_url_path = app.config.get('STATIC_FOLDER_PATH')
#	app.static_folder=app.root_path + app.static_url_path
	
	mongo.init_app(app)

	login_manager.init_app(app)
	bcrypt.init_app(app)
	# mail.init_app(app)

	from app.blueprints.errors.handlers import error_bp
	app.register_blueprint(error_bp)

	from app.blueprints.main.views import main
	app.register_blueprint(main)

	from app.blueprints.auth.routes import auth
	app.register_blueprint(auth)


	@app.template_filter()
	def format_date(given_date):
		return given_date.strftime('%H:%M:%S, %d-%B-%Y')

	return app

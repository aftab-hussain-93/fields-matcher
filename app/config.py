import os
import json
# UPLOADS_FOLDER = r'D:\development\project - fields matcher\uploads'

basedir = os.path.abspath(os.path.dirname(__file__))

with open('/etc/config.json') as config_file:
	config = json.load(config_file)

class Config:
	SECRET_KEY = config.get('SECRET_KEY')
	# SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
	SQLALCHEMY_DATABASE_URI = r"sqlite:///test.db"
	UPLOAD_FOLDER = ".data/uploads"
	DOWNLOAD_FOLDER = "./data/downloads"
	MAX_CONTENT_LENGTH = 16 * 1024 * 102
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	TEMP_FILES = "./data/temp_files"


	   #  SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #     'sqlite:///' + os.path.join(basedir, 'app.db')
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    # LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    # MAIL_SERVER = os.environ.get('MAIL_SERVER')
    # MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    # MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # ADMINS = ['your-email@example.com']
    # LANGUAGES = ['en', 'es']
    # MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')
    # ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
    # POSTS_PER_PAGE = 25

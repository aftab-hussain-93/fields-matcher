import os
# UPLOADS_FOLDER = r'D:\development\project - fields matcher\uploads'


class Config:
	SECRET_KEY = 'secret key'
	# SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
	SQLALCHEMY_DATABASE_URI = r"sqlite:///D:\development\project - fields matcher\app\test.db"
	UPLOAD_FOLDER = ".data/uploads"
	DOWNLOAD_FOLDER = "./data/downloads"
	MAX_CONTENT_LENGTH = 16 * 1024 * 102
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	TEMP_FILES = "./data/temp"
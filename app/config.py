import os
# UPLOADS_FOLDER = r'D:\development\project - fields matcher\uploads'


class Config:
	SECRET_KEY = 'secret key'
	SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
	UPLOAD_FOLDER = "uploads"
	DOWNLOAD_FOLDER = "downloads"
	MAX_CONTENT_LENGTH = 16 * 1024 * 102
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	TEMP_FILES = "temp"
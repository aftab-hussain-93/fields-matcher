import os

UPLOADS_FOLDER = r'D:\development\project - fields matcher\uploads'
class Config:
    SECRET_KEY = 'secret key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    UPLOAD_FOLDER = UPLOADS_FOLDER
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

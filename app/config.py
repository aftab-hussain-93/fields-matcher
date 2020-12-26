import os, pathlib
import json

basedir = os.path.abspath(os.path.dirname(__file__))
config = {}

try:
   with open('/etc/config.json') as config_file:
      config = json.load(config_file)
except FileNotFoundError:
   pass

class Config:
   #STATIC_FOLDER_PATH = pathlib.Path().parent + 'ui/static'
   SECRET_KEY = config.get('SECRET_KEY') or os.environ.get('SECRET_KEY')
   UPLOAD_FOLDER = "fieldsmatcher/uploads/"
   DOWNLOAD_FOLDER = "fieldsmatcher/downloads/"
   MAX_CONTENT_LENGTH = 4 * 1024 * 1024 # 4 mb file
   TEMP_FILES = "fieldsmatcher/tempfiles/"
   MONGO_URI = config.get('MONGO_URI') or os.environ.get('MONGO_URI')
   UPLOAD_EXTENSIONS = ['.csv','.xls','.xlsx','.json']
   AWS_SECRET_ACCESS_KEY = config.get('AWS_SECRET_ACCESS_KEY') or os.environ.get('AWS_SECRET_ACCESS_KEY')
   AWS_ACCESS_KEY_ID = config.get('AWS_ACCESS_KEY_ID') or os.environ.get('AWS_ACCESS_KEY_ID')
   AWS_BUCKET = "lunaflaskbucket"
   AWS_REGION = "ap-south-1"
   LOG_TO_STDOUT = config.get('LOG_TO_STDOUT') or os.environ.get('LOG_TO_STDOUT')
   MAIL_SERVER = config.get('MAIL_SERVER') or os.environ.get('MAIL_SERVER')
   MAIL_PORT =  config.get('MAIL_PORT') or int(os.environ.get('MAIL_PORT') or 25)
   MAIL_USE_TLS =  config.get('MAIL_USE_TLS') or os.environ.get('MAIL_USE_TLS') is not None
   MAIL_USERNAME = config.get('MAIL_USERNAME') or os.environ.get('MAIL_USERNAME')
   MAIL_PASSWORD = config.get('MAIL_PASSWORD') or os.environ.get('MAIL_PASSWORD')




	   #  SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #     'sqlite:///' + os.path.join(basedir, 'app.db')
    # SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ADMINS = ['your-email@example.com']
    # LANGUAGES = ['en', 'es']
    # MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')
    # ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
    # POSTS_PER_PAGE = 25

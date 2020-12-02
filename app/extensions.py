from flask_login import LoginManager
# from flask_httpauth import HTTPBasicAuth
# from flask_bcrypt import Bcrypt
# from flask_mail import Mail

login = LoginManager()
login.login_view = 'auth.login'
login.login_message_category = 'info'
# httpauth = HTTPBasicAuth()
# bcrypt = Bcrypt()
# mail = Mail()

from flask_pymongo import PyMongo

mongo = PyMongo()
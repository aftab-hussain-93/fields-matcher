from flask_login import LoginManager

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

# from flask_httpauth import HTTPBasicAuth
# httpauth = HTTPBasicAuth()

# from flask_mail import Mail
# mail = Mail()



from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()


from flask_pymongo import PyMongo

mongo = PyMongo()
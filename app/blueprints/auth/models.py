from app import db, login
import os
from flask import current_app
from app.blueprints.api.models import File
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class Base(db.Model):
	__abstract__ = True

	id = db.Column(db.Integer, primary_key=True)
	date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
	date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class User(Base, UserMixin):
	username = db.Column(db.String, nullable=False)
	password = db.Column(db.String, nullable=False)
	email = db.Column(db.String, nullable=False)

	uploaded_files = db.relationship('File', backref='user',lazy='dynamic')

	updated_files = db.relationship('UpdatedFile', backref='user',lazy=True)

	def get_login_token(self, expires_sec=1800):
		s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
		return s.dumps({'user_id':self.id}).decode('utf-8')

	@staticmethod
	def verify_token(token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			user_id = s.loads(token)['user_id']
		except:
			return None
		return User.query.get(user_id)
		
	def __repr__(self):
		return f"Username - {self.username}"

import os, uuid
from flask import current_app
from flask_login import UserMixin
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app.extensions import login_manager, mongo, bcrypt

@login_manager.user_loader
def load_user(pub_id):
	user = mongo.db.users.find_one({'public_id': pub_id})
	if user is not None:
		return User(**user)
	else:
		return None

class User(UserMixin):

	def __init__(self, email, password_hash, public_id=None, uploaded_files=None, _id=None):
		self.public_id = uuid.uuid4().hex if public_id is None else public_id
		self.email = email
		self.password_hash = password_hash
		self.uploaded_files = [] if uploaded_files is None else uploaded_files

	def get_id(self):
		return self.public_id

	@classmethod
	def get_by_email(cls, email):
		data = mongo.db.users.find_one({"email": email})
		if data is not None:
			return cls(**data)

	@classmethod
	def get_by_id(cls, pub_id):
		data = mongo.db.users.find_one({"public_id": pub_id})
		if data is not None:
			return cls(**data)

	def add_file_to_user(self, file_id):
		"""Method to append a file to User's uploaded_files list.

		Args:
			file_id ([type]): [description]
		"""
		user = mongo.db.users.find_one({"public_id": self.public_id})
		files = user['uploaded_files']
		files = [file_id] if not files else files.append(file_id)
		user['uploaded_files'] = files
		mongo.db.users.save(user)
		# return 

	def add_user_to_db(self):
		user_dict = {
			'public_id': self.public_id,
			'email' : self.email,
			'password_hash' : self.password_hash,
			'uploaded_files' : self.uploaded_files
		}

		result = mongo.db.users.insert_one(user_dict)
		current_app.logger.info(f"User added to Mongo. Inserted ID {result.inserted_id} ...")
		return result.inserted_id

	@staticmethod
	def login_valid(email, password):
		verify_user = User.get_by_email(email)
		if verify_user is not None:
			if bcrypt.check_password_hash(verify_user.password_hash, password):
				return verify_user
		return False


# class Base(db.Model):
# 	__abstract__ = True

# 	id = db.Column(db.Integer, primary_key=True)
# 	date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
# 	date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

# class User(Base, UserMixin):
# 	username = db.Column(db.String, nullable=False)
# 	password = db.Column(db.String, nullable=False)
# 	email = db.Column(db.String, nullable=False)

# 	uploaded_files = db.relationship('File', backref='user',lazy='dynamic')

# 	updated_files = db.relationship('UpdatedFile', backref='user',lazy=True)

# 	def get_login_token(self, expires_sec=1800):
# 		s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
# 		return s.dumps({'user_id':self.id}).decode('utf-8')

# 	@staticmethod
# 	def verify_token(token):
# 		s = Serializer(current_app.config['SECRET_KEY'])
# 		try:
# 			user_id = s.loads(token)['user_id']
# 		except:
# 			return None
# 		return User.query.get(user_id)

# 	def __repr__(self):
# 		return f"Username - {self.username}"

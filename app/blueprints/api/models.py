from app import db
from flask import current_app
import os

class Base(db.Model):
	__abstract__ = True

	id = db.Column(db.Integer, primary_key=True)
	date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
	date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class File(Base):
	filename = db.Column(db.String(128), nullable=False)
	directory = db.Column(db.String, nullable=False)
	public_id = db.Column(db.String(40), unique=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return f"File - {self.filename} - Directory - {self.directory}"
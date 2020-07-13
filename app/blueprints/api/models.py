from app import db
from flask import current_app
import os, uuid 

class Base(db.Model):
	__abstract__ = True

	id = db.Column(db.Integer, primary_key=True)
	date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
	date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class BaseFile(Base):
	__abstract__ = True

	filename = db.Column(db.String(150), nullable=False)
	public_id = db.Column(db.String(40), unique=True)
	directory = db.Column(db.String, nullable=False)

	@property	
	def file_path(self):
		return os.path.join(os.path.normpath(current_app.root_path), self.directory, self.filename)

class File(BaseFile):			
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	heading = db.relationship('Heading', backref='file', lazy=True)
	updated_files = db.relationship('UpdatedFile', backref='file', lazy=True)

	def __repr__(self):
		return f"File - {self.filename} - Directory - {self.directory}"

	def __init__(self, header_list=None, *args, **kwargs):
		if header_list:
			for i,head in enumerate(header_list,start=1):
				head = Heading(name=head,position=i, file=self)
				self.heading.append(head)
		super(File,self).__init__(*args, **kwargs)

	def generate_update_file(self, filename, directory):
		update_file = UpdatedFile(filename=filename, file=self, public_id=uuid.uuid4().hex, directory=directory, user_id=self.user_id)
		return update_file


class Heading(Base):
	name = db.Column(db.String(128), nullable=False)
	position = db.Column(db.Integer, nullable=False)
	file_id = db.Column(db.Integer, db.ForeignKey('file.id'))

	def __repr__(self):
		return f"Heading"

class UpdatedFile(BaseFile):
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	file_id = db.Column(db.Integer, db.ForeignKey('file.id'))

	# heading = db.relationship('Heading', backref='file', lazy=True)

	def __repr__(self):
		return f"File - {self.filename} - Directory - {self.directory}"

	def generate_update_file(self, filename, directory):
		update_file = UpdatedFile(filename=filename, file_id=self.file_id, public_id=uuid.uuid4().hex, directory=directory, user_id=self.user_id)
		return update_file
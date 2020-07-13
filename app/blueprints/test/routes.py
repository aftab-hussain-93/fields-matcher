from flask import Blueprint, current_app, jsonify
from app import db
from app.blueprints.auth.models import User
from app.blueprints.api.models import File, UpdatedFile


test = Blueprint('test',__name__,url_prefix = "/testing")

@test.route("/users")
def all_users():
	with current_app.app_context():
		all_users = User.query.all()
	all_usernames = [x.username for x in all_users]
	return jsonify(all_usernames), 200

@test.route("/files")
def all_files():
	with current_app.app_context():
		all_files = File.query.all()
		all_files = [(x.public_id, x.user.username if x.user else "no user" , x.file_path) for x in all_files]
	return jsonify(all_files), 200

@test.route("/updated_files")
def all_ufiles():
	with current_app.app_context():
		all_ufiles = UpdatedFile.query.all()
		all_files = [(x.public_id, x.user.username if x.user else "no user" , x.file_path) for x in all_ufiles]

	return jsonify(all_files), 200

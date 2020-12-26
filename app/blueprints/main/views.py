import os, json, uuid, pandas, boto3, io
from bson.objectid import ObjectId
from flask import (Blueprint, send_from_directory, request, session,
                    current_app, redirect, url_for, render_template, flash, abort, Response)
from flask_login import current_user
from app.blueprints.main.forms import UploadForm
from app.extensions import mongo
from app.models import User
from app.utils.aws_utils import AWSBucket
from app.utils.file_manipulation import File


main = Blueprint('main',__name__)

@main.route('/index', methods = ['GET', 'POST'])
@main.route('/', methods = ['GET', 'POST'])
def home():
	# flash(url_for('static'),"success")
	form = UploadForm()
	aws = AWSBucket(current_app._get_current_object())
	if form.validate_on_submit():
		current_app.logger.info("Form validated")
		uploaded_file = form.file.data

		if current_user.is_authenticated:
			file_path = current_app.config['UPLOAD_FOLDER'] + f'{current_user.public_id}/'
			user_id = current_user.public_id
		else:
			file_path = current_app.config['TEMP_FILES']
			user_id = None

		f = File(user_id, file_path)

		result = f.generate_new_file_doc(uploaded_file)
		file_document_dict = result['file_document']

		aws.file_upload(file=result['file_object'], key=file_document_dict['file_path'])
		current_app.logger.info(f"New file uploaded to S3\nKey - {file_document_dict['file_path']}")

		file_collection = mongo.db.uploaded_files
		_id = file_collection.insert_one(file_document_dict)
		current_app.logger.info(f"File added to Database\nID - {_id.inserted_id}")
		if current_user.is_authenticated:
			current_user.add_file_to_user(_id.inserted_id)
		return redirect(url_for('main.file_details', file_id=_id.inserted_id))
	else:
		current_app.logger.info(form.errors)
	return render_template('index.html', form=form)

@main.route('/file/<file_id>')
def file_details(file_id):
	current_file = mongo.db.uploaded_files.find_one({'_id': ObjectId(file_id)})
	if current_file['user_id']:
		if current_user.is_anonymous:
			abort(401)
		else:
			if current_user.public_id != current_file['user_id']:
				abort(401)
	elif current_user.is_authenticated:
		abort(401)
	extension = os.path.splitext(current_file['unique_name'])[1]
	original_file_attachment = current_file['original_filename'] + extension
	return render_template('dashboard.html',
		headings=current_file['headers'],
		file=current_file,
		file_id=file_id,
		original_file_attachment=original_file_attachment,
		filename=current_file['original_filename'])


@main.route('/delete/file/<file_id>')
def delete_file(file_id):
	files_collection = mongo.db.uploaded_files
	current_file = files_collection.find_one({'_id': ObjectId(file_id)})
	if current_file['user_id']:
		if current_user.is_anonymous:
			abort(401)
		else:
			if current_user.public_id != current_file['user_id']:
				abort(401)
	elif current_user.is_authenticated:
		abort(401)
	
	# Deleting Item from DB
	# Finding all children files
	child_files = files_collection.find({'parent_file_oid':  ObjectId(file_id)})
	aws = AWSBucket(current_app._get_current_object())

	current_app.logger.info("Deleting Child files from AWS")
	for child in child_files:
		current_app.logger.info(f"Deleting {child['unique_name']}")
		files_collection.remove({"_id": child["_id"]})
		aws.delete_bucket_item(key=child['file_path'])
	
	current_app.logger.info("Deleting main file")
	files_collection.remove({"_id": ObjectId(file_id)})
	aws.delete_bucket_item(key=current_file['file_path'])

	current_app.logger.info("Deleting app from mongo and then from AWS")
	current_app.logger.info("multithreading can be used here")
	current_app.logger.info("redirecting to hiome")
	return redirect(url_for('main.home'))

@main.route('/testing')
def testing():
	aws = AWSBucket(current_app._get_current_object())
	s3 = aws.get_client()
	return aws.list_bucket_items(s3)

@main.route('/modify_file', methods=['POST'])
def modify():
	"""
	"""

	data = request.get_json()
	file_id = data.get('file_id')
	new_extension = data.get('extension').lower() # None Type Error
	new_extension = File.sanitize_extension(new_extension)
	headers = data['headers'] # Key Error
	current_app.logger.debug(f"File ID- {file_id} \nExtension - {new_extension} \nHeader list- {headers} \n...")
	position_dict = {}
	header_name_dict = {}
	for head, details in headers.items():
		header_name_dict[head] = details['header_name']
		position_dict[head] = details['position']
	new_header_list = [x[0] for x in sorted(position_dict.items(), key=lambda x:x[1])]

	# Getting current file from DB.
	file_collection = mongo.db.uploaded_files
	current_file = file_collection.find_one({'_id': ObjectId(file_id)})

	## TO-DO -
	# Put check to ensure same user is accessing the file
	# if current_user.public_id == current_file.user_id:
	# if session['user_id'] == current_user.public_id == current_file.user_id
	# abort (404) unauthorized error

	current_file_path = current_file.get('file_path')
	name, extension = os.path.splitext(os.path.basename(current_file_path))
	ext = extension.split('.')[-1].lower()
	ext = File.sanitize_extension(ext)
	update_file_obj = File(user_id=current_file['user_id'], file_path=current_app.config['DOWNLOAD_FOLDER'] + '123/')

	# Downloading the original file from the S3 bucket.
	# Creating the dataframe of the file

	aws = AWSBucket(current_app._get_current_object())
	df = aws.aws_to_dataframe(key=current_file_path, extension=ext)

	# Modifying the data frame Adding the new modified headers
	try:
		df = df[new_header_list]  # NoneType/AttributeError if Dataframe has not been formed

	except AttributeError:
		current_app.logger.debug("Dataframe is not created. Extension provided incorrect.")
		raise Exception("Dataframe not created. The file uploaded is invalid.")

	# Modifying the data frame Renaming the headers
	df.rename(columns=header_name_dict,inplace=True)
	current_app.logger.debug("Dataframe modified")

	result = update_file_obj.generate_update_file_df(data_frame=df, current_file=current_file, new_extension=new_extension)
	new_file_document = result['file_document']
	s3_key = new_file_document['file_path']

	#### Uploading onto S3
	aws.put_file(body=result['file_object'].getvalue(), key=s3_key)
	current_app.logger.info(f"New file uploaded to S3\nKey - {s3_key}")

	#### Adding the Updated File document to the Database
	# Add file document to the database
	_id = file_collection.insert_one(new_file_document)
	# Append new files object id into the versions of the parent file
	parent_file = file_collection.find_one({'_id': ObjectId(new_file_document['parent_file_oid'])})
	versions = parent_file.get('versions')
	versions.append(_id.inserted_id)
	file_collection.save(parent_file)
	current_app.logger.info(f"New file object added to the database\nID - {_id.inserted_id}")

	return {
		'key': s3_key,
		'attachment_name': f'{new_file_document["original_filename"]}.{new_extension}'
		}, 200

@main.route('/download_file', methods=['POST'])
def download_file():
	aws = AWSBucket(current_app._get_current_object())
	key = request.form['key']
	attachment_name = request.form['attachment_name']
	return Response(
		aws.get_object(key),
		mimetype='text/plain',
		headers={"Content-Disposition": f"attachment; filename={attachment_name}"}
	)

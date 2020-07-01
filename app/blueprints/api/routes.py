import pandas
import os
import uuid 
from .models import File
from app.blueprints.auth.models import User 
from app import db, httpauth, bcrypt
from werkzeug.utils import secure_filename
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app.utils import modify_headers,  allowed_file, get_file_details
from flask import Blueprint, send_from_directory, request, current_app, make_response, jsonify

api = Blueprint('api',__name__, url_prefix = "/api/v1.0")

@api.route('/upload', methods=['POST'])
def api_upload():
    if 'file' not in request.files:
        resp = {
        'message':'No file part in request'
        }
        status = 400
        return resp, status

    file = request.files['file']

    if file.filename == '':
        resp = {
            'message':'No file selected for upload'
        }
        status = 400
        return resp, status

    if file and allowed_file(file.filename):
        file_id = uuid.uuid4().hex
        token = request.args.get('token')
        if token:
            current_user = User.verify_token(token)
            if current_user:
                DIRECTORY = os.path.join(current_app.config['UPLOAD_FOLDER'],current_user.username)
                path = os.path.join(os.path.normpath(current_app.root_path),DIRECTORY)
                if not os.path.exists(path):
                    os.makedirs(path)
                f = File(filename = file.filename, directory=DIRECTORY, public_id=file_id, user=current_user)
            else:
                resp = {
                    'error':'Invalid or expired token'
                }
                status = 400
                return resp, status
        else:
            DIRECTORY = current_app.config['TEMP_FILES']
            f = File(filename = file.filename, directory=DIRECTORY, public_id=file_id)
        
        filename = secure_filename(file.filename)
        file_path = os.path.join(os.path.normpath(current_app.root_path),DIRECTORY,filename)
        file.save(file_path)
        file.stream.seek(0)
        headers, extension = get_file_details(file)
        db.session.add(f)
        db.session.commit() 
        headers_w_position = {}
        for i,head in enumerate(headers,start=1):
            headers_w_position[head] = {
                'header_name' : head,
                'position' : i
            }
        resp = {
            'file_id': file_id,
            'extension' : extension,
            'headers' : headers_w_position
        }
        status = 201
        return resp, status
    else:
        resp = {
            'message' : 'File type not allowed'
        }
        status = 400
        return resp, status

@api.route('/modify',methods=['POST'])
def api_modify():
    data = request.get_json()
    if not data:
        return {'error':'No data provided'}, 400
    file_id = data.get('file_id')
    if not file_id:
        return {'error':'File ID not provided'}, 400
    file_obj = File.query.filter_by(public_id=file_id).first()
    if not file_obj:
        return {'error':'No such file exists.'}, 400
    extension = data.get('extension')
    if not extension:
        return {'error':'Extension not provided.'}, 400
    token = request.args.get('token')
    current_file = File.query.filter_by(public_id = file_id).first()
    if token:
        current_user = User.verify_token(token)        
        if current_file.user != current_user:
            return {'error':'Incorrect token provided'}, 400
    else:
        if current_file.user:
            return {'error':'File belongs to user. Please provide token'}, 400
    headers = data['headers']
    position_dict = {}
    header_name_dict = {}
    for head, details in headers.items():
        header_name_dict[head] = details['header_name']
        position_dict[head] = details['position']
    if len(position_dict.values()) != len(set(position_dict.values())):
        resp = {
            'message' : 'The position values provided are overlapping.'
        }
        status = 400
        return resp, status

    if any(i<=0 for i in position_dict.values()):
        return {'error':'The positions must contain values > 0'}, 400

    if max(position_dict.values()) > len(position_dict.values()):
        return {'error':'The maximum position exceeds the range'}, 400

      
    new_name = modify_headers(file_obj, extension, position_dict, header_name_dict)
    with current_app.app_context():
        download_folder = os.path.join(os.path.normpath(current_app.root_path), current_app.config['DOWNLOAD_FOLDER'])
    return send_from_directory(download_folder, new_name, as_attachment=True), 200


@httpauth.error_handler
def unauthorized():
    return make_response(jsonify({'message': 'Unauthorized'}), 403)

@httpauth.verify_password
def verify_password(username, password):
    if username:
        user = User.query.filter_by(username=username).first()
        if bcrypt.check_password_hash(user.password, password):
            return user

@api.route('/login')
@httpauth.login_required
def api_login():
    usr = httpauth.current_user()
    token = usr.get_login_token()
    return {
        'token' : token
    }

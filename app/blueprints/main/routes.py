# from main import main
from flask import (Blueprint, send_from_directory, request, session, 
                    current_app, redirect, url_for, render_template, flash)
from app.utils import  get_file_headers, modify_headers, allowed_file, get_user_files
from app.blueprints.api.routes import api
from app.blueprints.api.models import File, UpdatedFile
from flask_login import current_user
import os
import json

main = Blueprint('main',__name__)

@main.route('/index', methods = ['GET'])
@main.route('/', methods = ['GET'])
def home():
    """
    Home page to upload the file. The file upload is handled by JQuery AJAX Form.
    """
    if current_user.is_authenticated:
        flash(f'Hello {current_user.username}', category='info')
    return render_template('home.html')

@main.route('/modify', methods=['POST'])
def modify_file():
    """
    After file upload, the page with all the details. Called by JQuery Ajax call.
    """
    file_id = request.form['file_id']
    current_file = File.query.filter_by(public_id=file_id).first()
    if not current_file:
        current_file = UpdatedFile.query.filter_by(public_id=file_id).first()
    filename = current_file.filename
    headers, extension = get_file_headers(current_file)
    current_app.logger.info(f"Modifying file - {file_id}")
    return render_template('modify.html', headings=headers, file_id=file_id, filename=filename, extension=extension)

@main.route('/download', methods=['POST'])
def download():
    print(f"Downloading file name")
    filename = request.form['filename']
    # return "hello"
    with current_app.app_context():
        download_folder = os.path.join(os.path.normpath(current_app.root_path), current_app.config['DOWNLOAD_FOLDER'])
    return send_from_directory(download_folder, filename, as_attachment=True)
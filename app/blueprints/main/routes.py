# from main import main
from flask import (send_from_directory, request, session, 
                    current_app, redirect, url_for, render_template)
from app.utils import  get_file_headers, modify_headers, allowed_file
from app.blueprints.api.routes import api
from app.blueprints.api.models import File
from flask import Blueprint
import os

main = Blueprint('main',__name__)

@main.route('/index', methods = ['GET'])
@main.route('/', methods = ['GET'])
def upload_file():
    """
    Home page to upload the file. The file upload is handled by JQuery AJAX Form.
    """
    current_app.logger.info("In home page")
    return render_template('home.html')

@main.route('/modify', methods=['POST'])
def modify_file():
    """
    After file upload, the page with all the details. Called by JQuery Ajax call.
    """
    file_id = request.form['file_id']
    current_file = File.query.filter_by(public_id=file_id).first()
    filename = current_file.filename
    headers, extension = get_file_headers(current_file)
    current_app.logger.info(f"Modifying file - {file_id}")
    return render_template('modify.html', headings=headers, file_id=file_id, filename=filename, extension=extension)

@main.route('/api/download/<filename>')
def api_download(filename):
    print(f"Downloading file name {filename}")
    with current_app.app_context():
        download_folder = os.path.join(os.path.normpath(current_app.root_path), current_app.config['DOWNLOAD_FOLDER'])
    return send_from_directory(download_folder, filename, as_attachment=True)
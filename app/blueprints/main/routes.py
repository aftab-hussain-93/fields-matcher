import os, json, uuid, pandas
from flask import (Blueprint, send_from_directory, request, session,
                    current_app, redirect, url_for, render_template, flash)
from app.blueprints.main.forms import UploadForm
from app.utils import modify_headers,  allowed_file, get_file_details, get_file_headers, get_user_files
from app.blueprints.api.routes import api
from app.blueprints.api.models import File, UpdatedFile
from flask_login import current_user
from app import db


main = Blueprint('main',__name__)

@main.route('/index', methods = ['GET', 'POST'])
@main.route('/', methods = ['GET', 'POST'])
def home():
    """
    Home page to upload the file using Upload Form. If form validated, the file is stored in directory and file details in DB.
    """
    form = UploadForm()
    if form.validate_on_submit():
        current_app.logger.info("Form validated")
        f = form.file.data

        # Generating Unique name for file for storage in the directory
        public_id = uuid.uuid4().hex
        original_filename = f.filename
        ext = original_filename.rsplit('.')[-1].lower()
        original_filename = os.path.splitext(original_filename)[0]
        unique_name = f"{public_id}.{ext}"

        # Choosing the storage directory
        if current_user.is_authenticated:
            DIRECTORY = os.path.join(current_app.config['UPLOAD_FOLDER'],current_user.username)
        else:
            DIRECTORY = current_app.config['TEMP_FILES']

        # Creating Folder for User if logged in, else storing file in Temp folder
        path = os.path.join(os.path.normpath(current_app.root_path),DIRECTORY)
        if not os.path.exists(path):
            os.makedirs(path)

        # File storage absolute path
        file_path = os.path.join(os.path.normpath(current_app.root_path),DIRECTORY,unique_name)
        current_app.logger.info(f"Saving file to file system..")
        current_app.logger.info(f"Path - {file_path}")
        # session['file_path'] = file_path
        # session['file_name'] = original_filename
        f.save(file_path)

        f.stream.seek(0)
        headers, extension = get_file_details(f)

        # TODO- Adding file to DB
        current_app.logger.info("Adding file details to the Database.")
        if current_user.is_authenticated:
            f = File(filename = original_filename, directory=file_path, public_id=public_id, user=current_user, header_list = headers)
        else:
            f = File(filename = original_filename, directory=file_path, public_id=public_id, header_list = headers)

        db.session.add(f)
        db.session.commit()
        flash(f"File uploaded","info")
        return render_template('dashboard.html', headings=headers, file_id=public_id, filename=original_filename, extension=extension)
    return render_template('index.html', form=form)

@main.route('/modify_file', methods=['POST'])
def modify():
    """[Function used to apply modification to the uploaded file. AJAX request accesses this function.]

    Returns:
        [type]: [description]
    """

    DOWNLOAD_FOLDER = os.path.join(os.path.normpath(current_app.root_path),current_app.config['DOWNLOAD_FOLDER'])

    print(f"The updated file headings are.")
    data = request.get_json()
    public_id = data.get('file_id') # File unique ID. public_id
    current_app.logger.debug(f"File public ID- {public_id} ")
    current_file = File.query.filter_by(public_id=public_id).first()
    current_app.logger.debug(f"Current File - {current_file} ")
    new_extension = data.get('extension')
    current_app.logger.debug(f"New Extension - {new_extension} ")
    new_extension = new_extension.lower()
    headers = data['headers']
    current_app.logger.debug(f"Header list- {headers}")
    position_dict = {}
    header_name_dict = {}
    for head, details in headers.items():
        header_name_dict[head] = details['header_name']
        position_dict[head] = details['position']

    ## TODO - Modfication of files

    new_header_list = [x[0] for x in sorted(position_dict.items(), key=lambda x:x[1])]
    current_file_path = current_file.directory
    name, extension = os.path.splitext(os.path.basename(current_file_path))
    ext = extension.split('.')[-1].lower()
    df = None
    if ext == 'csv':
        df = pandas.read_csv(current_file_path)
        current_app.logger.debug("File read and CSV dataframe created.")
    elif ext in ['xls','xlsx']:
        df = pandas.read_excel(current_file_path)
        current_app.logger.debug("File read and excel dataframe created.")
    df = df[new_header_list]
    df.rename(columns=header_name_dict,inplace=True)
    new_public_id = uuid.uuid4().hex
    if new_extension in ('csv','comma'):
        new_name = new_public_id + ".csv"
        updated_file_path = os.path.join(os.path.normpath(DOWNLOAD_FOLDER),new_name)
        df.to_csv(updated_file_path, index = False, header=True)
        current_app.logger.debug(f"File modified - {updated_file_path}")
    elif new_extension in ('excel','xls','xlsx'):
        new_name = new_public_id + ".xlsx"
        updated_file_path = os.path.join(os.path.normpath(DOWNLOAD_FOLDER),new_name)
        df.to_excel(updated_file_path, index = False, header=True)
        current_app.logger.debug(f"File modified - {updated_file_path}")
    updated_file = current_file.generate_update_file(public_id = new_public_id, file_path=updated_file_path)
    ## TODO - End

    # updated_file_path = os.path.join(os.path.normpath(current_app.root_path), updated_file.directory) # Not needed
    unique_name = updated_file.filename
    current_app.logger.info("Returning the NEW FILE")
    return {
        'path': updated_file_path,
        'filename': unique_name
        }, 200
    # return send_from_directory(updated_file_path,unique_name, as_attachment=True), 200

@main.route('/download_file', methods=['POST'])
def download_file():
    print(f"Downloading file name")
    filename = request.form['filename']
    path = request.form['path']
    directory = os.path.dirname(path)
    file_saved_name, ext = os.path.splitext(os.path.basename(path))
    print(file_saved_name)
    download_name = f"{filename}{ext}"
    # return "hello"
    return send_from_directory(directory, os.path.basename(path), as_attachment=True, attachment_filename = download_name)
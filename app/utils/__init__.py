import pandas, datetime, os
from werkzeug.utils import secure_filename
from flask import current_app


ALLOWED_EXTENSIONS = {'csv','xls','xlsx'}


# UPLOAD_FOLDER = r'D:\development\project - fields matcher\uploads'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.')[1].lower() in ALLOWED_EXTENSIONS

def save_file(file):
    """
    Saves the file to upload folder. Returns a list of headers, and filename.

    Args:
        file :  File to be upload. File object of request.
    """
    with current_app.app_context():
        UPLOAD_FOLDER = os.path.join(os.path.normpath(current_app.root_path), current_app.config['UPLOAD_FOLDER'])
        # UPLOAD_FOLDER = app.config['UPLOAD_FOLDER']
    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER,filename)
    file.save(file_path)
    return filename

def get_file_headers(filename):
    with current_app.app_context():
        UPLOAD_FOLDER = os.path.join(os.path.normpath(current_app.root_path), current_app.config['UPLOAD_FOLDER'])
    file_path = os.path.join(UPLOAD_FOLDER,filename)
    ext = filename.rsplit('.')[-1].lower()
    if ext == 'csv':
        df = pandas.read_csv(file_path)
    elif ext in ['xls','xlsx']:
        df = pandas.read_excel(file_path)
    headers = df.columns.to_list()
    return headers, ext

def change_file_extension(filename, new_extension):
    pass

def modify_headers(filename, extension, position_dict, name_dict):
    new_header_ls = [x[0] for x in sorted(position_dict.items(), key=lambda x:x[1])]
    print("The new header list is going to be")
    print(new_header_ls)
    name, ext = os.path.splitext(filename)
    ext = ext.split('.')[-1].lower()
    with current_app.app_context():
        UPLOAD_FOLDER = os.path.join(os.path.normpath(current_app.root_path), current_app.config['UPLOAD_FOLDER'])
        DOWNLOAD_FOLDER = os.path.join(os.path.normpath(current_app.root_path), current_app.config['DOWNLOAD_FOLDER'])
    file_path = os.path.join(os.path.normpath(UPLOAD_FOLDER),filename)
    if ext == 'csv':
        df = pandas.read_csv(file_path)
    elif ext in ['xls','xlsx']:
        df = pandas.read_excel(file_path)
    df = df[new_header_ls]
    df.rename(columns=name_dict,inplace=True)
    extension = extension.lower()
    now = datetime.datetime.now().strftime('%y%m%d%H%M%S')
    new_name = f'{name}{now}.{extension}'
    if extension in ('csv','comma'):
        df.to_csv(os.path.join(os.path.normpath(DOWNLOAD_FOLDER),new_name), index = False, header=True)
    elif extension in ('excel','xls','xlsx'):
        df.to_excel(os.path.join(os.path.normpath(DOWNLOAD_FOLDER),new_name), index = False, header=True)
    return new_name

# from main import main
from flask import send_from_directory, request, current_app, redirect, url_for, render_template
from app.utils import save_file, get_file_headers, modify_headers, allowed_file
from flask import Blueprint
import os

main = Blueprint('main',__name__)

@main.route('/index', methods = ['GET', 'POST'])
@main.route('/', methods = ['GET', 'POST'])
def upload_file():
    print("Hwerer")
    if request.method == 'POST':
        print("Check 1!!")
        print(request.files)
        if 'file' not in request.files:
            print('No File part')
            return redirect(request.url)
        file = request.files['file']
        print("Check 2!!")
        if file.filename == '':
            print("No selected file")
            return redirect(request.url)
        print("Check 3!!")
        if file and allowed_file(file.filename):
            filename = save_file(file)
            print("FIle saved redirecting")
            return redirect(url_for('main.modify_file', filename = filename))
    return '''
<!doctype html>
<title>Upload new File</title>
<h1>Upload new File</h1>
<form method=post enctype=multipart/form-data>
<input type=file name=file>
<input type=submit value=Upload>
</form>
'''

@main.route('/modify/<filename>', methods=['POST','GET'])
def modify_file(filename):
    headers, extension = get_file_headers(filename)
    return render_template('modify.html', headings = headers, filename = filename, extension = extension)


@main.route('/api/download/<filename>')
def api_download(filename):
    print(f"Downloading file name {filename}")
    with current_app.app_context():
        download_folder = os.path.join(os.path.normpath(current_app.root_path), current_app.config['DOWNLOAD_FOLDER'])
    return send_from_directory(download_folder, filename, as_attachment=True)
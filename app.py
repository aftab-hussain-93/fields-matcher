import os
import pandas
from collections import OrderedDict
from flask_wtf import FlaskForm
from wtforms import StringField
from flask import Flask, redirect, request, url_for,\
flash, send_from_directory, render_template, jsonify
from utils import save_file, get_file_headers, modify_headers


UPLOADS_FOLDER = r'D:\development\project - fields matcher\uploads'
ALLOWED_EXTENSIONS = {'csv','xls','xlsx'}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret key'
app.config['UPLOAD_FOLDER'] = UPLOADS_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.')[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No File part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash("No selected file")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = save_file(file)
            return redirect(url_for('modify_file', filename = filename))
    return '''
<!doctype html>
<title>Upload new File</title>
<h1>Upload new File</h1>
<form method=post enctype=multipart/form-data>
<input type=file name=file>
<input type=submit value=Upload>
</form>
'''

@app.route('/modify/<filename>', methods=['POST','GET'])
def modify_file(filename):
    headers, extension = get_file_headers(filename)
    class F(FlaskForm):
        pass
    for head in headers:
        setattr(F, head, StringField(f'{head}'))
    form = F()
    if form.validate_on_submit():
        print("Form data validated")
        return redirect(url_for('upload_file'))
    return render_template('modify.html', form = form, headings = headers)

@app.route('/api/upload', methods=['POST'])
def api_upload():
    if 'file' not in request.files:
        resp = jsonify({
            'message' : 'No file part in request'
        })
        resp.status_code = 400
        return resp
    file = request.files['file']
    if file.filename == '':
        resp = jsonify({
            'message':'No file selected for upload'
        })
        resp.status_code = 400
        return resp
    if file and allowed_file(file.filename):
        filename = save_file(file)
        headers, extension = get_file_headers(filename)
        headers_w_position = {}
        for i,head in enumerate(headers,start=1):
            headers_w_position[head] = {
                'header_name' : head,
                'position' : i
            }
        resp = jsonify({
            'filename': filename,
            'extension' : extension,
            'headers' : headers_w_position
        })
        resp.status_code = 201
        return resp
    else:
        resp = jsonify({
            'message' : 'File type not allowed'
        })
        resp.status_code = 400
        return resp

@app.route('/api/modify',methods=['POST'])
def api_modify():
    data = request.get_json()
    filename = data['filename']
    extension = data['extension']
    headers = data['headers']
    position_dict = {}
    header_name_dict = {}
    for head, details in headers.items():
        header_name_dict[head] = details['header_name']
        position_dict[head] = details['position']
    if len(position_dict.values()) != len(set(position_dict.values())):
        resp = jsonify({
            'message' : 'The position values provided are overlapping.'
        })
        resp.status_code = 400
        return resp
    else:
        new_name = modify_headers(filename, extension, position_dict, header_name_dict)
        return redirect(url_for('api_download', filename = new_name))


@app.route('/api/download/<filename>')
def api_download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)